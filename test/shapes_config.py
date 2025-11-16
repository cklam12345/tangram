"""
Tangram Target Shapes Configuration for tangram_game.py
Each shape contains pieces with center coordinates and rotation angles
"""

SHAPES = {
    "swan": {
        "name": "Swan",
        "difficulty": "medium",
        "pieces": [
            {
                "color": "red",
                "center": [305, 290],
                "angle": 225,
                "piece_type": "large_triangle"
            },
            {
                "color": "green",
                "center": [401, 320],
                "angle": 135,
                "piece_type": "medium_triangle"
            },
            {
                "color": "blue",
                "center": [346, 335],
                "angle": 180,
                "piece_type": "large_triangle"
            },
            {
                "color": "yellow",
                "center": [426, 280],
                "angle": 315,
                "piece_type": "small_triangle"
            },
            {
                "color": "purple",
                "center": [418, 165],
                "angle": 270,
                "piece_type": "small_triangle"
            },
            {
                "color": "teal",
                "center": [399, 241],
                "angle": 315,
                "piece_type": "square"
            },
            {
                "color": "orange",
                "center": [378, 186],
                "angle": 315,
                "piece_type": "parallelogram"
            },
        ]
    },


    
    "cat": {
        "name": "Cat",
        "difficulty": "easy",
        "pieces": [
            {
                "color": "red",
                "center": [250, 300],
                "angle": 0,
                "piece_type": "large_triangle"
            },
            {
                "color": "blue",
                "center": [350, 300],
                "angle": 0,
                "piece_type": "large_triangle"
            },
            {
                "color": "green",
                "center": [300, 200],
                "angle": 45,
                "piece_type": "medium_triangle"
            },
            {
                "color": "yellow",
                "center": [300, 250],
                "angle": 0,
                "piece_type": "square"
            },
            {
                "color": "orange",
                "center": [220, 180],
                "angle": 45,
                "piece_type": "small_triangle"
            },
            {
                "color": "purple",
                "center": [380, 180],
                "angle": 135,
                "piece_type": "small_triangle"
            },
            {
                "color": "teal",
                "center": [300, 150],
                "angle": 0,
                "piece_type": "parallelogram"
            }
        ]
    },
    
    "rocket": {
        "name": "Rocket",
        "difficulty": "hard",
        "pieces": [
            {
                "color": "red",
                "center": [300, 350],
                "angle": 0,
                "piece_type": "large_triangle"
            },
            {
                "color": "blue",
                "center": [300, 250],
                "angle": 0,
                "piece_type": "large_triangle"
            },
            {
                "color": "green",
                "center": [300, 150],
                "angle": 0,
                "piece_type": "medium_triangle"
            },
            {
                "color": "yellow",
                "center": [300, 200],
                "angle": 0,
                "piece_type": "square"
            },
            {
                "color": "orange",
                "center": [250, 380],
                "angle": 45,
                "piece_type": "small_triangle"
            },
            {
                "color": "purple",
                "center": [350, 380],
                "angle": 135,
                "piece_type": "small_triangle"
            },
            {
                "color": "teal",
                "center": [300, 100],
                "angle": 0,
                "piece_type": "small_triangle"
            }
        ]
    }
}

# Color mapping for piece identification (BGR format for OpenCV)
COLOR_MAP = {
    "red": (80, 80, 255),
    "blue": (255, 80, 80),
    "green": (80, 255, 80),
    "yellow": (80, 255, 255),
    "orange": (0, 165, 255),
    "purple": (255, 80, 255),
    "teal": (255, 255, 100)
}

# Piece type to size mapping
PIECE_TYPE_MAP = {
    "large_triangle": "large_tri",
    "medium_triangle": "medium_tri",
    "small_triangle": "small_tri",
    "square": "square",
    "parallelogram": "parallelogram"
,

    "custom": {
        "name": "Custom",
        "difficulty": "medium",
        "pieces": [
            {
                "color": "red",
                "center": [316, 350],
                "angle": 225,
                "piece_type": "large_triangle"
            },
            {
                "color": "green",
                "center": [412, 381],
                "angle": 135,
                "piece_type": "medium_triangle"
            },
            {
                "color": "blue",
                "center": [357, 397],
                "angle": 180,
                "piece_type": "large_triangle"
            },
            {
                "color": "yellow",
                "center": [436, 343],
                "angle": 315,
                "piece_type": "small_triangle"
            },
            {
                "color": "purple",
                "center": [430, 230],
                "angle": 270,
                "piece_type": "small_triangle"
            },
            {
                "color": "teal",
                "center": [411, 304],
                "angle": 315,
                "piece_type": "square"
            },
            {
                "color": "orange",
                "center": [392, 248],
                "angle": 315,
                "piece_type": "parallelogram"
            },
        ]
    },

}

# Piece sizes for game rendering
PIECE_SIZES = {
    "large_triangle": 60,
    "medium_triangle": 45,
    "small_triangle": 30,
    "square": 40,
    "parallelogram": 40
}

def get_shape(shape_name):
    """Get a shape configuration by name"""
    return SHAPES.get(shape_name, None)

def get_all_shapes():
    """Get all shapes (for tangram_game.py compatibility)"""
    return SHAPES

def get_shape_pieces(shape_name):
    """Get pieces list for a shape (for tangram_game.py compatibility)"""
    shape = SHAPES.get(shape_name)
    if shape:
        return shape.get("pieces", [])
    return []

def get_all_shape_names():
    """Get list of all available shape names"""
    return list(SHAPES.keys())

def get_shape_difficulty(shape_name):
    """Get difficulty level of a shape"""
    shape = SHAPES.get(shape_name)
    return shape["difficulty"] if shape else None
