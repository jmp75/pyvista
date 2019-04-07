"""
.. _ref_texture_example:

Applying Textures
~~~~~~~~~~~~~~~~~

Plot a mesh with an image projected onto it as a texture.
"""

################################################################################
# Texture mapping is easily implemented using ``vtki``. Many of the geometric
# objects come preloaded with texture coordinates, so quickly creating a surface
# and displaying an image is simply:

import vtki
from vtki import examples
import numpy as np

# load a sample texture
tex = examples.download_masonry_texture()

# create a surface to host this texture
surf = vtki.Cylinder()

surf.plot(texture=tex)


################################################################################
# But what if your dataset doesn't have texture coordinates? Then you can
# harness the :func:`vtki.DataSetFilters.texture_map_to_plane` filter to
# properly map an image to a dataset's surface.
# For example, let's map that same image of bricks to a curvey surface:

# create a structured surface
x = np.arange(-10, 10, 0.25)
y = np.arange(-10, 10, 0.25)
x, y = np.meshgrid(x, y)
r = np.sqrt(x**2 + y**2)
z = np.sin(r)
curvsurf = vtki.StructuredGrid(x, y, z)

# Map the curved surface to a plane - use best fitting plane
curvsurf.texture_map_to_plane(inplace=True)

curvsurf.plot(texture=tex)


################################################################################
# Note that this process can be completed with any image texture!

# use the puppy image
tex = examples.download_puppy_texture()
curvsurf.plot(texture=tex)


################################################################################
# What about loading your own texture from an image? This is often most easily
# done using the :func:`vtki.read_texture` function - simply pass an image
# file's path, and this function with handle making a ``vtkTexture`` for you to
# use.

image_file = examples.mapfile
tex = vtki.read_texture(image_file)
curvsurf.plot(texture=tex)


################################################################################
# Wan't to use a programmaticaly built image? :class:`vtki.UniformGrid` objects
# can be converted to textures using :func:`vtki.image_to_texture` and 3D
# NumPy (X by Y by RGB) arrays can be converted to textures using
# :func:`vtki.numpy_to_texture`.

# create an image using Numpy,
xx, yy = np.meshgrid(np.linspace(-200,200,20), np.linspace(-200,200,20))
A, b = 500, 100
zz = A*np.exp(-0.5*((xx/b)**2. + (yy/b)**2.))

# Creating a custom RGB image
from matplotlib.cm import get_cmap
cmap = get_cmap('nipy_spectral')
norm = lambda x: (x - np.nanmin(x)) / (np.nanmax(x) - np.nanmin(x))
hue = norm(zz.ravel())
colors = (cmap(hue)[:, 0:3] * 255.).astype(np.uint8)
image = colors.reshape((xx.shape[0], xx.shape[1], 3), order='F')

# Convert 3D numpy array to texture
tex = vtki.numpy_to_texture(image)

# Render it!
curvsurf.plot(texture=tex)
