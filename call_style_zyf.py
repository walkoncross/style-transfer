#!/usr/bin/env python
import style

model = 'googlenet'
#style = './images/style/mosaic-s.jpg'
#style = './images/style/starry_night.jpg'
#style = './images/style/huangbinhong.jpg'
style = './images/style/Monet_Sunrise.jpg'
#style = './images/style/Monet_Water_lilies.jpg'
#style = './images/style/Monet_Water_lilies2.jpg'
img = './images/content/zjg3.jpg'
#img = './zyf.jpg'
#output = ''
ratio = '1e4'
init = 'content'
iters = 100

input_args = '-m ' + model + ' -r ' + ratio + ' -s ' + style + ' -c ' + img + ' -i ' + init + ' -n ' + str(iters)

#runfile('C:/zyf/github/style-transfer/style.py', args=input_args, wdir='C:/zyf/github/style-transfer')
style.main(input_args.split())