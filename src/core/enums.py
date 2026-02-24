import enum


class WishlistVisibility(str, enum.Enum):
    public = "public"
    link_only = "link_only"
    private = "private"


class WishlistRole(str, enum.Enum):
    viewer = "viewer"
    editor = "editor"
