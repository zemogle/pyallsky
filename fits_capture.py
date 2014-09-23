from allsky import AllSkyCamera
import serial
import argparse, sys
import aplpy
from datetime import datetime

IMAGE_DIR = '/local/filesystem/path'

def capture_image(device, exposure_time, savefile):
    try:
        cam = AllSkyCamera(device)
        cam.open_shutter()
        print('Downloading image ...')
        image = cam.get_image(exposure=exposure_time)
        try:
            path = args.path            
        except AttributeError:
            filename = "image-%s.fits" % datetime.now().isoformat("T")
            path = os.join(IMAGE_DIR,filename)
        image.writeto(path)
        make_png(path)
    except serial.serialutil.SerialException as err:
        print(str(err))
        sys.exit(2)

def make_png(filename):
    fig = aplpy.FITSFigure(filename)
    fig.show_grayscale()
    filepng = filename.replace('.fits','.png')
    fig.save(filepng)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--device', help='Path to serial device', default='/dev/usbserial')
    parser.add_argument('-e', '--exposure', type=float, help='Exposure time in seconds', default=1.0)
    parser.add_argument('path', help='Filename to save image')
    args = parser.parse_args()
    capture_image(args.device, args.exposure, args.path)


if __name__ == '__main__':
    main()
