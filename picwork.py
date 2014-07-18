from PIL import Image, ImageDraw
import os
	
def transparent(fname,fname2):
	def isWhite(pix):
		buffer = 15
		return abs(pix[0]+pix[1]+pix[2]+pix[3]-255*4) <= buffer
	
	def three2four(p):
		return (p[0],p[1],p[2],255)
	print fname		
	im = Image.open(fname)
	w,h = im.size[0],im.size[1]
	if len(im.getpixel((0,0))) == 3:
		rgba = Image.new('RGBA',im.size)
		for i in range(w):
			for j in range(h):
				rgba.putpixel((i,j),three2four(im.getpixel((i,j))))
		im = rgba
	elif len(im.getpixel((0,0))) < 3:
		raise ValueError()
		
	stack = []
	for i in range(0,w,10):
		stack.append((i,0))
		stack.append((i,h-1))
	for j in range(0,h,10):	
		stack.append((0,j))
		stack.append((w-1,j))
	
	null = (255,255,255,0)
	t = 0
	t2 = len(stack)
	while len(stack):
		t += 1
		point = stack.pop()
		x,y = point[0],point[1]
		im.putpixel(point,null)
		try:
			if isWhite(im.getpixel((x+1,y))):
					stack.append((x+1,y))
		except: pass
		try:
			if isWhite(im.getpixel((x-1,y))):
				stack.append((x-1,y))
		except: pass
		try:
			if isWhite(im.getpixel((x,y+1))):
				stack.append((x,y+1))
		except: pass
		try:
			if isWhite(im.getpixel((x,y-1))):
				stack.append((x,y-1))
		except: pass

	os.remove(fname)
	im.save(fname2+'.png', 'PNG')
	return t - t2 
#transparent("cartoon bear.jpg")
