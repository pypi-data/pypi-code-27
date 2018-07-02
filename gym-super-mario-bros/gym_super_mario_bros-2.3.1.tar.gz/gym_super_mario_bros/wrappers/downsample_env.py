"""An environment wrapper for down-sampling frames from RGB to smaller B&W."""
import gym
import cv2
import numpy as np


class DownsampleEnv(gym.ObservationWrapper):
    """An environment that down-samples frames."""

    def __init__(self, env: gym.Env, image_size: tuple):
        """
        Create a new down-sampler.

        Args:
            env: the environment to wrap
            image_size: the size to output frames as (width X height)

        Returns:
            None

        """
        super().__init__(env)
        self.image_size = image_size
        # set up a new observation space
        self.observation_space = gym.spaces.Box(
            low=0,
            high=255,
            shape=(image_size[1], image_size[0], 1),
            dtype=np.uint8
        )

    def observation(self, frame: np.ndarray) -> np.ndarray:
        """
        Downsample an observation from RGB to gray scale and resize it

        Args:
            frame: the image to convert to grayscale and resize

        Returns:
            the frame in B&W and resized to self.image_size

        """
        # convert the frame from RGB to gray scale
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # resize the frame to the expected shape. use bilinear interpolation
        frame = cv2.resize(frame, self.image_size)

        return frame[:, :, np.newaxis]


# explicitly define the outward facing API of this module
__all__ = [DownsampleEnv.__name__]
