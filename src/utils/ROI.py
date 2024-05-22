import numpy as np
from roifile import ImagejRoi, ROI_TYPE, ROI_OPTIONS
from src.utils.coordinate_system import Point


class ROI:
    """Represents a region of interest (ROI). This is a rectangle which specifies a certain region of an image."""
    WIDTH_PIXELS: int = None  # the width of all ROIs in pixels
    HEIGHT_PIXELS: int = None  # the height of all ROIs in pixels

    N_HORIZONTAL: int = None  # the number of ROIs along the x-axis
    N_VERTICAL: int = None  # the number of ROIs along the y-axis

    # TODO this should probably go somewhere else but when I put it in options, it caused a circular import
    PIXELS_PER_MM: float = None  # the number of pixels per millimeter in the calcium image

    @classmethod
    @property
    def width_mm(cls) -> float:
        """The width in millimeters"""
        return cls.WIDTH_PIXELS / cls.PIXELS_PER_MM

    @classmethod
    @property
    def height_mm(cls) -> float:
        """The height in millimeters"""
        return cls.HEIGHT_PIXELS / cls.PIXELS_PER_MM

    def __init__(self, x_idx, y_idx):
        self.x_idx = x_idx  # the x index on the grid of ROIs
        self.y_idx = y_idx

    def __str__(self):
        return self.compact_label()

    def __repr__(self):
        # return f'<ROI(x:{self.x_idx}; y:{self.y_idx}) at {str(hex(id(self)))}>'
        return f'ROI({self.x_idx};{self.y_idx})'

    @classmethod
    def from_linear_index(cls, linear_index: int):
        x_idx = linear_index % cls.N_VERTICAL
        y_idx = linear_index // cls.N_VERTICAL
        return cls(x_idx, y_idx)

    def linear_index(self) -> int:
        # The horizontal index is always the first dimension and vertical the second
        return self.x_idx * ROI.N_VERTICAL + self.y_idx

    def compact_label(self) -> str:
        return f"({self.x_idx};{self.y_idx})"

    def filename(self) -> str:
        # we want the number of digits for each number to be the same as the maximum number of digits for readability
        max_digits = max(len(str(ROI.N_HORIZONTAL)), len(str(ROI.N_VERTICAL)))
        x_formatted = f'{self.x_idx:0{max_digits}d}'
        y_formatted = f'{self.y_idx:0{max_digits}d}'
        file_name = f'({x_formatted}; {y_formatted}).roi'
        return file_name

    def imagej_label(self) -> str:
        return f'Mean(({self.x_idx}; {self.y_idx}))'

    def corners_pixels(self) -> tuple[Point, Point]:
        """Returns the upper left and lower right corners of the ROI as Point objects. The corner points and edges \
        should be *included* in the ROI"""
        x_ul = self.x_idx * ROI.WIDTH_PIXELS  # upper left x
        y_ul = self.y_idx * ROI.HEIGHT_PIXELS  # upper left y
        x_lr = x_ul + ROI.WIDTH_PIXELS - 1  # lower right x
        y_lr = y_ul + ROI.HEIGHT_PIXELS - 1  # lower right y

        return Point(x_ul, y_ul), Point(x_lr, y_lr)

    def center_pixels(self) -> Point:
        """Returns the center of the ROI as a Point object."""
        x = self.x_idx * ROI.WIDTH_PIXELS + ROI.WIDTH_PIXELS / 2 - 0.5
        y = self.y_idx * ROI.HEIGHT_PIXELS + ROI.HEIGHT_PIXELS / 2 - 0.5
        return Point(x, y)

    def corners_mm(self) -> Point:
        """Returns the upper left and lower right corners (in millimeters) of the ROI as Point objects."""
        # upper left corner:
        x_ul = self.x_idx * ROI.width_mm
        y_ul = self.y_idx * ROI.height_mm
        # lower right corner:
        x_lr = x_ul + ROI.width_mm
        y_lr = y_ul + ROI.height_mm
        return Point(x_ul, y_ul), Point(x_lr, y_lr)

    def center_mm(self) -> Point:
        """Returns the center of the ROI in millimeters."""
        x_idx_center = self.x_idx + 0.5
        y_idx_center = self.y_idx + 0.5

        return Point(
            x_idx_center * ROI.width_mm,
            y_idx_center * ROI.height_mm
        )

    # noinspection PyPep8Naming
    def as_ImagejRoi(self):
        p0, p1 = self.corners_pixels()
        roi = ImagejRoi.frompoints(np.array([[p0.x, p0.y], [p1.x, p1.y]]))
        roi.roitype = ROI_TYPE.RECT
        roi.name = self.compact_label()
        roi.options |= ROI_OPTIONS.OVERLAY_LABELS
        roi.options |= ROI_OPTIONS.SHOW_LABELS
        return roi
