from threading import Condition, Event, Thread
from time import sleep
from cv2 import VideoCapture
from cv2.typing import MatLike

class Camera: 
  def __init__(self, index: int = 0) -> None:
    self._cap: VideoCapture = VideoCapture(
      index,
      # CAP_V4L2
    )
    
    self._halt: Event = Event()

    self._frame_id: int = 0
    self._frame: MatLike | None = None
    self._frame_condition: Condition = Condition() 

    self._cap_loop_thread: Thread = Thread(target=self._cap_loop, daemon=True)
    self._cap_loop_thread.start()

  def _cap_loop(self):
    while not self._halt.is_set():
      ok, frame = self._cap.read()
      if ok:
        with self._frame_condition:
          self._frame = frame
          self._frame_id += 1
          self._frame_condition.notify_all()
      else:
        sleep(1/60)

  def getFrame(self):
    with self._frame_condition:
      return None if self._frame is None else self._frame.copy()

  def release(self):
    self._halt.set()

    with self._frame_condition:
      self._frame_condition.notify_all()

    self._cap.release()