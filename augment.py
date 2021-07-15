import rawpy, imageio, glob, os
import augly.image as imaugs
 
# install in this order
# pip install python-magic-bin==0.4.14
# pip install augly
 
# Imgpath = name of raw picture (specify path if image is not in same project directory) (extensions could be .CR2,.raw )
# ProcessedImgType: Specify the extension of processed image (png,JPEG, etc...)
# n_augments: number of augmentations to perform for original RAW image. Default is 5 augmentations
# (each augmentation takes on average 6 seconds to complete)
def AugmentRawImage(Imgpath, ProcessedImgType = 'jpg', n_augments=5):
  
  rawImg = rawpy.imread(Imgpath)
  rgbImg = rawImg.postprocess()
 
  imageio.imsave(f'{Imgpath}_Processed.{ProcessedImgType}', rgbImg)
  rawImg.close()
 
  input_img = imaugs.scale(f'{Imgpath}_Processed.{ProcessedImgType}',factor=1)
 
  aug_list =[]
  for i in range(0,n_augments):
      aug = imaugs.Compose(
          [
              imaugs.RandomAspectRatio(),
              imaugs.RandomBrightness(min_factor=0.1),
              imaugs.RandomBlur(),
              imaugs.RandomPixelization(),
              imaugs.RandomRotation(),
              imaugs.RandomNoise()
          ]
      )
      aug_list.append(aug)
      
      imaugs.scale(aug_list[i](input_img),factor=1,
                  output_path= f'{Imgpath}_Augmented{i}.{ProcessedImgType}')
 
def AugmentDir(dirpath, ProcessedImgType = 'jpg', n_augments=5):
    for img in glob.glob(os.path.join(dirpath, "*")):
        AugmentRawImage(img, ProcessedImgType = ProcessedImgType, n_augments = n_augments)

AugmentDir("libs/fish/raw/", ProcessedImgType = 'jpg', n_augments=10)