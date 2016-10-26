import png
r = png.Reader('photo.png')
ans = r.read()
print ans
