import glm
import pygame


import engine.context as ctx
import engine.constants as consts

from engine.physics import entity

# ======================================================================== #
# Camera
# ======================================================================== #


class BaseCamera(entity.Entity):
    def __init__(self, render_distance: int):
        super().__init__()

        self._render_distance = render_distance


# ======================================================================== #
# 2D Camera
# ======================================================================== #


class Camera2D(BaseCamera):
    def __init__(self, render_distance: int):
        super().__init__(render_distance)

        self._chunk_pos = (0, 0)

    # ------------------------------------------------------------------------ #
    # logic
    # ------------------------------------------------------------------------ #

    def generate_visible_chunks(self):
        self._chunk_pos = (
            self._position.x // consts.DEFAULT_CHUNK_PIXEL_WIDTH,
            self._position.y // consts.DEFAULT_CHUNK_PIXEL_HEIGHT,
        )
        # generate visible chunks
        for x in range(-self._render_distance, self._render_distance):
            for y in range(-self._render_distance, self._render_distance):
                yield (x + self._chunk_pos[0], y + self._chunk_pos[1])


# ======================================================================== #
# 3D Camera
# ======================================================================== #


class Camera3D(BaseCamera):
    def __init__(
        self,
        render_distance: int,
        fov: float = 45,
        near: float = 0.1,
        far: float = 1000,
        position: glm.vec3 = glm.vec3(0, 0, 0),
        up: glm.vec3 = glm.vec3(0, 1, 0),
        forward: glm.vec3 = glm.vec3(0, 0, 1),
        orthogonal: bool = False,
    ):
        super().__init__(render_distance)

        self._fov = fov
        self._near = near
        self._far = far
        self._position = position
        self._up = up
        self._forward = forward
        self._orthogonal = orthogonal

        # view matrix
        self._view = glm.lookAt(
            self._position,
            self._position + self._forward,
            glm.cross(consts.GLM_Constants.RIGHT, self._forward),
        )

        # create projection -- default is perspective
        self.calculate_projection()

    # ------------------------------------------------------------------------ #
    # logic
    # ------------------------------------------------------------------------ #

    def calculate_projection(self):
        if self._orthogonal:
            self._projection = glm.ortho(
                -consts.W_SURFACE.get_width() / 2,
                consts.W_SURFACE.get_width() / 2,
                -consts.W_SURFACE.get_height() / 2,
                consts.W_SURFACE.get_height() / 2,
                self._near,
                self._far,
            )
        else:
            self._projection = glm.perspective(
                glm.radians(self._fov),
                consts.W_SURFACE.get_width() / consts.W_SURFACE.get_height(),
                self._near,
                self._far,
            )

    # ------------------------------------------------------------------------ #
    # properties
    # ------------------------------------------------------------------------ #

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        self._view = glm.lookAt(
            self._position,
            self._position + self._forward,
            glm.cross(consts.GLM_Constants.RIGHT, self._forward),
        )

    @property
    def target(self):
        return self._position + self._forward

    @target.setter
    def target(self, value):
        self._forward = value - self._position
        self._view = glm.lookAt(
            self._position,
            self._position + self._forward,
            glm.cross(consts.GLM_Constants.RIGHT, self._forward),
        )

    @property
    def forward(self):
        return self._forward

    @forward.setter
    def forward(self, value):
        self._forward = value
        self._view = glm.lookAt(
            self._position,
            self._position + self._forward,
            glm.cross(consts.GLM_Constants.RIGHT, self._forward),
        )


# ======================================================================== #
# Camera Utils
# ======================================================================== #


def calculate_forward_from_target(position: glm.vec3, target: glm.vec3):
    return target - position
