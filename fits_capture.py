from allsky import AllSkyCamera
import serial
import argparse, sys, shutil
import f2n
import ephem
from datetime import datetime

IMAGE_DIR = '/home/pi/fits/'
LAT ='51.924984'
LON = '-3.4885652'

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
	latest = os.join(IMAGE_DIR,"latest.jpg")
	shutil.copy(path,latest)
    except serial.serialutil.SerialException as err:
        print(str(err))
        sys.exit(2)

def twilight(lat,lon):
    ''' Returns True is viewing location is in darkness '''
    now = datetime.now().strftime("%Y/%m/%d %H:%M")
    brecon = ephem.Observer()
    brecon.lat, brecon.lon = lat, lon
    brecon.horizon = '-12' # set to Nautical Twilight
    rise = brecon.next_rising(ephem.Sun(), use_center=True)
    sunset = brecon.previous_setting(ephem.Sun(), use_center=True)
    rise_tp = rise.tuple()
    rise_dt = datetime(rise_tp[0],rise_tp[1],rise_tp[2],rise_tp[3],rise_tp[4])
    sunset_tp = sunset.tuple()
    sunset_dt = datetime(sunset_tp[0],sunset_tp[1],sunset_tp[2],sunset_tp[3],sunset_tp[4])
    if rise - sunset > 1.0:
        # In this case we're getting Sunset from the previous day and it is currently day
        return False
    elif sunset_dt <= now and rise_tp >= now:
        return True
    else:
        return False

def make_png(filename):
    myimage = f2n.fromfits(filename)
    myimage.makepilimage("log", negative = False)
    try:
        filepng = filename.replace('.fits','.png')
        myimage.tonet(filepng)
    except Exception, err:
        print(str(err))
        sys.exit(2)
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--device', help='Path to serial device', default='/dev/usbserial')
    parser.add_argument('-e', '--exposure', type=float, help='Exposure time in seconds', default=1.0)
    parser.add_argument('path', help='Filename to save image')
    args = parser.parse_args()
    if twilight(LAT,LON):
        capture_image(args.device, args.exposure, args.path)


if __name__ == '__main__':
    main()
