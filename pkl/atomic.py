# package pkl

# import (
# 	"math/rand"
# 	"sync"
# 	"time"
# )

# type atomicBool struct {
# 	mutex sync.Mutex
# 	value bool
# }

# func (a *atomicBool) get() bool {
# 	a.mutex.Lock()
# 	defer a.mutex.Unlock()
# 	return a.value
# }

# func (a *atomicBool) set(value bool) {
# 	a.mutex.Lock()
# 	defer a.mutex.Unlock()
# 	a.value = value
# }

# type atomicRandom struct {
# 	mutex sync.Mutex
# 	rand  *rand.Rand
# }

# func (a *atomicRandom) Int63() int64 {
# 	a.mutex.Lock()
# 	defer a.mutex.Unlock()
# 	return a.rand.Int63()
# }

# var random = &atomicRandom{
# 	rand: rand.New(rand.NewSource(time.Now().UnixMilli())),
# }

import dataclasses
import random
import threading
import time


@dataclasses.dataclass
class AtomicBool:
    value: bool = False
    mutex: threading.Lock = dataclasses.field(default_factory=threading.Lock)

    def get(self):
        with self.mutex:
            return self.value

    def set(self, value):
        with self.mutex:
            self.value = value


@dataclasses.dataclass
class AtomicRandom:
    rand: random.Random = dataclasses.field(
        default_factory=lambda: random.Random(time.time())
    )
    mutex: threading.Lock = dataclasses.field(default_factory=threading.Lock)

    def Int63(self):
        with self.mutex:
            return self.rand.randint(0, 2**63 - 1)


random_var = AtomicRandom(rand=random.Random(time.time()))
