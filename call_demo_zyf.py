#!/usr/bin/env python
import demo

model = 'googlenet'
#style = './images/style/mosaic-s.jpg'
style = './images/style/starry_night.jpg'
#style = './images/style/Monet-Sunrise-bright.jpg'
#style = './images/style/halloween.jpg'
#style = './images/style/halloween_pumpkins.jpg'
#style = './images/style/halloween.jpg'
#style = './images/style/joker2.jpg'
#style = './images/style_nightmare/capitol_toxic.png'
#style = './images/style_nightmare/colosseum_haunted.png'
#style = './images/style_nightmare/london_inferno.png'
#style = './images/style_nightmare/newyork_frightnight.png'
#style = './images/style_nightmare/stonehenge_ghost.png'
#style = './images/style/Monet_Water_lilies.jpg'
#style = './images/style/Monet_Water_lilies2.jpg'
#img = './images/content/guodegang.jpg'
#img = './images/content/sanfrancisco.jpg'
#img = './images/content/johannesburg.jpg'
#img = './images/content/nanjing.jpg'
img = './images/content/zjg3.jpg'
#img = './zyf.jpg'
#output = ''
ratio = '1e4'
init = 'content'

input_args = '-m ' + model + ' -r ' + ratio + ' -s ' + style + ' -c ' + img + ' -i ' + init

#runfile('C:/zyf/github/style-transfer/demo.py', args=input_args, wdir='C:/zyf/github/style-transfer')
#runfile('./demo.py', args=input_args, wdir='./')
demo.main(input_args.split())
#runfile('C:/zyf/github/style-transfer/demo.py', args='-m googlenet -r 1e4 -s ./images/style/picasso.jpg -c ./images/content/nanjing.jpg', wdir='C:/zyf/github/style-transfer')