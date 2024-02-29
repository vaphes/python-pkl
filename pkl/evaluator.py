# package pkl

# import (
# 	"context"
# 	"fmt"
# 	"log"
# 	"net/url"
# 	"sync"

# 	"github.com/apple/pkl-go/pkl/internal/msgapi"
# )

# // Evaluator is an interface for evaluating Pkl modules.
# type Evaluator interface {
# 	// EvaluateModule evaluates the given module, and writes it to the value pointed by
# 	// out.
# 	//
# 	// This method is designed to work with Go modules that have been code generated from Pkl
# 	// sources.
# 	EvaluateModule(ctx context.Context, source *ModuleSource, out any) error

# 	// EvaluateOutputText evaluates the `output.text` property of the given module.
# 	EvaluateOutputText(ctx context.Context, source *ModuleSource) (string, error)

# 	// EvaluateOutputValue evaluates the `output.value` property of the given module,
# 	// and writes to the value pointed by out.
# 	EvaluateOutputValue(ctx context.Context, source *ModuleSource, out any) error

# 	// EvaluateOutputFiles evaluates the `output.files` property of the given module.
# 	EvaluateOutputFiles(ctx context.Context, source *ModuleSource) (map[string]string, error)

# 	// EvaluateExpression evaluates the provided expression on the given module source, and writes
# 	// the result into the value pointed by out.
# 	EvaluateExpression(ctx context.Context, source *ModuleSource, expr string, out interface{}) error

# 	// EvaluateExpressionRaw evaluates the provided module, and returns the underlying value's raw
# 	// bytes.
# 	//
# 	// This is a low level API.
# 	EvaluateExpressionRaw(ctx context.Context, source *ModuleSource, expr string) ([]byte, error)

# 	// Close closes the evaluator and releases any underlying resources.
# 	Close() error

# 	// Closed tells if this evaluator is closed.
# 	Closed() bool
# }

# type evaluator struct {
# 	evaluatorId     int64
# 	logger          Logger
# 	manager         *evaluatorManager
# 	pendingRequests *sync.Map
# 	closed          bool
# 	resourceReaders []ResourceReader
# 	moduleReaders   []ModuleReader
# }

# var _ Evaluator = (*evaluator)(nil)

# func (e *evaluator) EvaluateModule(ctx context.Context, source *ModuleSource, out any) error {
# 	return e.EvaluateExpression( source, "", out)
# }

# func (e *evaluator) EvaluateOutputText(ctx context.Context, source *ModuleSource) (string, error) {
# 	var out string
# 	err := e.EvaluateExpression( source, "output.text", &out)
# 	return out, err
# }

# func (e *evaluator) EvaluateOutputValue(ctx context.Context, source *ModuleSource, out any) error {
# 	return e.EvaluateExpression(ctx, source, "output.value", out)
# }

# func (e *evaluator) EvaluateOutputFiles(ctx context.Context, source *ModuleSource) (map[string]string, error) {
# 	var out map[string]string
# 	err := e.EvaluateExpression(ctx, source, "output.files.toMap().mapValues((_, it) -> it.text)", &out)
# 	return out, err
# }

# func (e *evaluator) EvaluateExpression(ctx context.Context, source *ModuleSource, expr string, out interface{}) error {
# 	bytes, err := e.EvaluateExpressionRaw(ctx, source, expr)
# 	if err != nil {
# 		return err
# 	}
# 	return Unmarshal(bytes, out)
# }

# func (e *evaluator) EvaluateExpressionRaw(ctx context.Context, source *ModuleSource, expr string) ([]byte, error) {
# 	if e.Closed() {
# 		return nil, fmt.Errorf("evaluator is closed")
# 	}
# 	requestId := random.Int63()
# 	ch := make(chan *msgapi.EvaluateResponse)
# 	e.pendingRequests.Store(requestId, ch)
# 	interrupted, nevermind := e.manager.interrupted(e.evaluatorId)
# 	defer nevermind()
# 	e.manager.impl.outChan() <- &msgapi.Evaluate{
# 		RequestId:   requestId,
# 		ModuleUri:   source.Uri.String(),
# 		ModuleText:  source.Contents,
# 		Expr:        expr,
# 		EvaluatorId: e.evaluatorId,
# 	}
# 	select {
# 	case <-ctx.Done():
# 		return nil, nil
# 	case err := <-interrupted:
# 		return nil, err
# 	case resp := <-ch:
# 		if resp.Error != "" {
# 			return nil, &EvalError{ErrorOutput: resp.Error}
# 		}
# 		return resp.Result, nil
# 	}
# }

# func (e *evaluator) Close() error {
# 	if e.closed {
# 		return nil
# 	}
# 	e.manager.closeEvaluator(e)
# 	return nil
# }

# func (e *evaluator) Closed() bool {
# 	return e.closed
# }

# func (e *evaluator) handleEvaluateResponse(resp *msgapi.EvaluateResponse) {
# 	c, exists := e.pendingRequests.Load(resp.RequestId)
# 	if !exists {
# 		log.Default().Printf("warn: received a message for an unknown request id: %d", resp.RequestId)
# 		return
# 	}
# 	ch := c.(chan *msgapi.EvaluateResponse)
# 	ch <- resp
# 	close(ch)
# 	e.pendingRequests.Delete(resp.RequestId)
# }

# func (e *evaluator) handleLog(resp *msgapi.Log) {
# 	switch resp.Level {
# 	case 0:
# 		e.logger.Trace(resp.Message, resp.FrameUri)
# 	case 1:
# 		e.logger.Warn(resp.Message, resp.FrameUri)
# 	default:
# 		// log level beyond 1 is impossible
# 		panic(fmt.Sprintf("unknown log level: %d", resp.Level))
# 	}
# }

# func (e *evaluator) handleReadResource(msg *msgapi.ReadResource) {
# 	response := &msgapi.ReadResourceResponse{EvaluatorId: e.evaluatorId, RequestId: msg.RequestId}
# 	u, err := url.Parse(msg.Uri)
# 	if err != nil {
# 		response.Error = fmt.Errorf("internal error: failed to parse resource url: %w", err).Error()
# 		e.manager.impl.outChan() <- response
# 		return
# 	}
# 	var reader ResourceReader
# 	for _, r := range e.resourceReaders {
# 		if r.Scheme() == u.Scheme {
# 			reader = r
# 			break
# 		}
# 	}
# 	if reader == nil {
# 		response.Error = fmt.Sprintf("No resource reader found for scheme `%s`", u.Scheme)
# 		e.manager.impl.outChan() <- response
# 		return
# 	}
# 	contents, err := reader.Read(*u)
# 	response.Contents = contents
# 	if err != nil {
# 		response.Error = err.Error()
# 	}
# 	e.manager.impl.outChan() <- response
# }

# func (e *evaluator) handleReadModule(msg *msgapi.ReadModule) {
# 	response := &msgapi.ReadModuleResponse{EvaluatorId: e.evaluatorId, RequestId: msg.RequestId}
# 	u, err := url.Parse(msg.Uri)
# 	if err != nil {
# 		response.Error = fmt.Errorf("internal error: failed to parse resource url: %w", err).Error()
# 		e.manager.impl.outChan() <- response
# 		return
# 	}
# 	var reader ModuleReader
# 	for _, r := range e.moduleReaders {
# 		if r.Scheme() == u.Scheme {
# 			reader = r
# 			break
# 		}
# 	}
# 	if reader == nil {
# 		response.Error = fmt.Sprintf("No module reader found for scheme `%s`", u.Scheme)
# 		e.manager.impl.outChan() <- response
# 		return
# 	}
# 	response.Contents, err = reader.Read(*u)
# 	if err != nil {
# 		response.Error = err.Error()
# 	}
# 	e.manager.impl.outChan() <- response
# }

# func (e *evaluator) handleListResources(msg *msgapi.ListResources) {
# 	response := &msgapi.ListResourcesResponse{EvaluatorId: e.evaluatorId, RequestId: msg.RequestId}
# 	u, err := url.Parse(msg.Uri)
# 	if err != nil {
# 		response.Error = fmt.Errorf("internal error: failed to parse resource url: %w", err).Error()
# 		e.manager.impl.outChan() <- response
# 		return
# 	}
# 	var reader ResourceReader
# 	for _, r := range e.resourceReaders {
# 		if r.Scheme() == u.Scheme {
# 			reader = r
# 			break
# 		}
# 	}
# 	if reader == nil {
# 		response.Error = fmt.Sprintf("No resource reader found for scheme `%s`", u.Scheme)
# 		e.manager.impl.outChan() <- response
# 		return
# 	}
# 	pathElements, err := reader.ListElements(*u)
# 	if err != nil {
# 		response.Error = err.Error()
# 	} else {
# 		for _, pathElement := range pathElements {
# 			response.PathElements = append(response.PathElements, &msgapi.PathElement{
# 				Name:        pathElement.Name(),
# 				IsDirectory: pathElement.IsDirectory(),
# 			})
# 		}
# 	}
# 	e.manager.impl.outChan() <- response
# }

# func (e *evaluator) handleListModules(msg *msgapi.ListModules) {
# 	response := &msgapi.ListModulesResponse{EvaluatorId: e.evaluatorId, RequestId: msg.RequestId}
# 	u, err := url.Parse(msg.Uri)
# 	if err != nil {
# 		response.Error = fmt.Errorf("internal error: failed to parse resource url: %w", err).Error()
# 		e.manager.impl.outChan() <- response
# 		return
# 	}
# 	var reader ModuleReader
# 	for _, r := range e.moduleReaders {
# 		if r.Scheme() == u.Scheme {
# 			reader = r
# 			break
# 		}
# 	}
# 	if reader == nil {
# 		response.Error = fmt.Sprintf("No module reader found for scheme `%s`", u.Scheme)
# 		e.manager.impl.outChan() <- response
# 		return
# 	}
# 	pathElements, err := reader.ListElements(*u)
# 	if err != nil {
# 		response.Error = err.Error()
# 	} else {
# 		for _, pathElement := range pathElements {
# 			response.PathElements = append(response.PathElements, &msgapi.PathElement{
# 				Name:        pathElement.Name(),
# 				IsDirectory: pathElement.IsDirectory(),
# 			})
# 		}
# 	}
# 	e.manager.impl.outChan() <- response
# }

# type simpleEvaluator struct {
# 	Evaluator
# 	manager EvaluatorManager
# }

# var _ Evaluator = (*simpleEvaluator)(nil)

# func (rcv *simpleEvaluator) Close() error {
# 	return rcv.manager.Close()
# }

import dataclasses

from pkl.evaluator_manager import EvaluatorManager
from pkl.logger import Logger
from pkl.module_source import ModuleSource
from pkl.reader import ModuleReader, ResourceReader


@dataclasses.dataclass
class Evaluator:
    manager: EvaluatorManager
    evaluator_id: int
    resource_readers: list[ResourceReader]
    module_readers: list[ModuleReader]
    logger: Logger

    def evaluate_module(self, source: ModuleSource, out):
        return self.evaluate_expression(source, "", out)

    def evaluate_output_text(self, source):
        out = ""
        err = self.evaluate_expression(source, "output.text", out)
        return out, err

    def evaluate_output_value(self, source, out):
        return self.evaluate_expression(source, "output.value", out)

    def evaluate_output_files(self, source):
        out = {}
        err = self.evaluate_expression(
            source, "output.files.toMap().mapValues((_, it) -> it.text)", out
        )
        return out, err

    def evaluate_expression(self, source, expr, out):
        bytes, err = self.evaluate_expression_raw(source, expr)
        if err:
            return err
        return self.unmarshal(bytes, out)

    def evaluate_expression_raw(self, source, expr):
        if self.closed:
            return None, "evaluator is closed"
        request_id = random.randint(0, 1000000000)
        ch = {}
        self.pendingRequests[request_id] = ch
        interrupted, nevermind = self.manager.interrupted(self.evaluatorId)
        e.manager.impl.out_chan() < -{
            "RequestId": request_id,
            "ModuleUri": source.uri.string(),
            "ModuleText": source.contents,
            "Expr": expr,
            "EvaluatorId": self.evaluatorId,
        }
        if ctx.done():
            return None, None
        if interrupted:
            return None, interrupted
        if ch:
            if ch["Error"]:
                return None, ch["Error"]
            return ch["Result"], None

    def close(self):
        if self.closed:
            return None
        self.manager.close_evaluator(self.evaluator_id)
        return None

    def closed(self):
        return self.closed

    def handle_evaluate_response(self, resp):
        c = self.pendingRequests[resp["RequestId"]]
        if not c:
            print(
                "warn: received a message for an unknown request id:", resp["RequestId"]
            )
            return
        ch = c
        ch < -resp
        ch.close()
        self.pendingRequests.pop(resp["RequestId"])

    def handle_log(self, resp):
        if resp["Level"] == 0:
            self.logger.trace(resp["Message"], resp["FrameUri"])
        elif resp["Level"] == 1:
            self.logger.warn(resp["Message"], resp["FrameUri"])
        else:
            raise Exception(f"unknown log level: {resp['Level']}")

    def handle_read_resource(self, msg):
        response = {"EvaluatorId": self.evaluatorId, "RequestId": msg["RequestId"]}
        u = url.parse(msg["Uri"])
        if not u:
            response["Error"] = f"internal error: failed to parse resource url: {u}"
            self.manager.impl.out_chan() < -response
            return
        reader = None
        for r in self.resourceReaders:
            if r.scheme() == u.scheme:
                reader = r
                break
        if not reader:
            response["Error"] = f"No resource reader found for scheme `{u.scheme}`"
            self.manager.impl.out_chan() < -response
            return
        contents, err = reader.read(u)
        response["Contents"] = contents
        if err:
            response["Error"] = err
        self.manager.impl.out_chan() < -response

    def handle_read_module(self, msg):
        response = {"EvaluatorId": self.evaluatorId, "RequestId": msg["RequestId"]}
        u = url.parse(msg["Uri"])
        if not u:
            response["Error"] = f"internal error: failed to parse resource url: {u}"
            self.manager.impl.out_chan() < -response
            return
        reader = None
        for r in self.moduleReaders:
            if r.scheme() == u.scheme:
                reader = r
                break
        if not reader:
            response["Error"] = f"No module reader found for scheme `{u.scheme}`"
            self.manager.impl.out_chan() < -response
            return
        response["Contents"], err = reader.read(u)
        if err:
            response["Error"] = err
        self.manager.impl.out_chan() < -response

    def handle_list_resources(self, msg):
        response = {"EvaluatorId": self.evaluatorId, "RequestId": msg["RequestId"]}
        u = url.parse(msg["Uri"])
        if not u:
            response["Error"] = f"internal error: failed to parse resource url: {u}"
            self.manager.impl.out_chan() < -response
            return
        reader = None
        for r in self.resourceReaders:
            if r.scheme() == u.scheme:
                reader = r
                break
        if not reader:
            response["Error"] = f"No resource reader found for scheme `{u.scheme}`"
            self.manager.impl.out_chan() < -response
            return
        path_elements, err = reader.list_elements(u)
        if err:
            response["Error"] = err
        else:
            for path_element in path_elements:
                response["PathElements"].append(
                    {
                        "Name": path_element.name(),
                        "IsDirectory": path_element.is_directory(),
                    }
                )
        self.manager.impl.out_chan() < -response

    def handle_list_modules(self, msg):
        response = {"EvaluatorId": self.evaluatorId, "RequestId": msg["RequestId"]}
        u = url.parse(msg["Uri"])
        if not u:
            response["Error"] = f"internal error: failed to parse resource url: {u}"
            self.manager.impl.out_chan() < -response
            return
        reader = None
        for r in self.moduleReaders:
            if r.scheme() == u.scheme:
                reader = r
                break
        if not reader:
            response["Error"] = f"No module reader found for scheme `{u.scheme}`"
            self.manager.impl.out_chan() < -response
            return
        path_elements, err = reader.list_elements(u)
        if err:
            response["Error"] = err
        else:
            for path_element in path_elements:
                response["PathElements"].append(
                    {
                        "Name": path_element.name(),
                        "IsDirectory": path_element.is_directory(),
                    }
                )
        self.manager.impl.out_chan() < -response


@dataclasses.dataclass
class SimpleEvaluator:
    Evaluator: Evaluator
    manager: EvaluatorManager

    def close(self):
        return self.manager.close()
