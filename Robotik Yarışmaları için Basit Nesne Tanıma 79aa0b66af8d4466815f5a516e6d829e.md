# Robotik Yarışmaları için Basit Nesne Tanıma

## Projenin temel hedefleri:

- Düşük donanımlı sistemlerde çalışmalı
- Gerçek zamanlı görüntü işleyebilmeli

# Yaklaşım:

## Renk özelliğini kullanarak nesne tanıma

Robotik yarışmalarında hedefler genellikle renk değerleriyle öne çıkan hedefler olduğu için nesne tespitinde renk özelliğin kullanarak maskeleme yapmak en kolay yaklaşım olacaktır.

**HSV:**

HSV objenin hue, saturation ve value değerlerini gösteren bir renk şema sistemidir. HSV renk şemasında ortam ışığına bağlı olarak sadece saturation ve value değerlerinde farklılık gösterdiği için renk özelliğinde maskeleme yapmak için kullanımı daha verimli olacaktır.

Alt ve üst sınırlarını belirlediğimiz hsv değerleri maskelememizin ilk adımını oluşturur

**Opening**:

Elde ettiğimiz maskede aslında ayrık olan alanlar ufak değerlerle birbiri ile birleşik gözükebilmektedir. Böyle nesneleri biribirinden ayırmak için erozyon ve korozyon operasyonlarını art arda kullanan opening fonksiyonunu kullanmak nesnelerin ayrılmasını sağlayacaktır

**Median Filter:**

Maskeleme ve opening operasyonlarının ardından maskeyi parazitlerden arındırmak şekillerin kenar çizgilerini bulmayı kolaylaştırmaktadır.

Elde edilen maskede görevin gerekliliklerine göre çeşitli filtrelemeler kullanılabilir. Örneğin duba tespit etmek için alanların yuvarlaklığı kıyaslanabilir. Çoğu görevde olabilecek ortak bir filtreleme ise nesnenin alan büyüklüğü olabilir. Görev esnasında kameraya en yakın obje, tespit etmek istenilen obje ise algılanan alanlar arasında en büyükleri üzerinden işlem yapmak işlem süresini kısaltır.

Renk özelliğinden yola çıkarak elde edilen ROI’leri algoritmanın doğruluk açısından güçlendirilmesi için bir katman daha filtreleme eklenebilir

### Şekil özelliğini kullanarak filtreleme

Renk değerlerini alınan obje özel bir reflektör renge boyanmadıysa ortamın ışıklandırmasından dolayı objenin şekliyle birebir uyuşmayabilir. Bundan dolayı ilk katman filtrelemeden elde edilen alana gerçek resim üzerinden şekil özelliğini değerlendiren bir katman eklenebilir

- Canny edge detector:
    
    Aşağıdaki 5 adımdan oluşan canny edge detector ile ROI içindeki nesne yuvarlaklığı üzerinden değerlendirilebilir
    
    1. Gaussian filtre ile görüntüyü yumuşatma
    2. Resmin gradyan yoğunluğunu hesaplama (bkz. sobel operator)
    3. NMS ile yanlış kenarları silme
    4. Gradyan yoğunluğunu treshold ile alt ve üst sınırlarını belirleyerek filtreleme
    5. Hysteresis kullanarak güçlü kenarlara bağlanmayan zayıf kenarları silme

### CNN kullanarak

- Siyah Beyaz model eğitimi*
    
    Bir görsel sınıflandırma modeli eğiterek belirlenen ROI’lerin duba barındırıp barındırmadığı tespit edilebilir
    
    ROI’ler renklerden tespit edildiği için renkli görüntü kullanılması yerine daha küçük bir modelin kullanılabilmesini sağlamak için veri setinde siyah beyaz görüntü kullanılabilir. 
    
- Binary görsel model eğitimi
    
    Siyah Beyaz yerine modelimizi binary görüntülerden oluşan bir veri seti eğitilip performansları karşılaştırılabilir
    

## CNN ile nesne tanıma

Performans açısından donanıma ve göreve uygun olarak mobil CNN modelleri kullanarak nesne tespiti yapılabilir. Hız açısından daha hızlı ama doğruluğu daha az modeller tercih edilebileceği gibi daha yavaş ama daha doğru modelleri hızlandırmak da tercih edilebilir.

Modelimizin hızını arttırmak için :

- Tek cisim ise:
    - Siyah beyaz model eğitilebilir
    - Renk özelliklerini kullanarak uyguladığımız filtrelemeyi yapıp buradan veri seti oluşturarak binary görüntüden model eğitilebilir
- Birden çok cisim ise
    - Siyah beyaz model eğitilebilir. Nesneyi tespit ettikten sonra elde ettiğimiz çerçeve içindeki rengi algılayabiliriz
    

# Metot 1.0 : Renk özellikleri

## Kullanılan Fonksiyonlar

```python
def masking(img, lower_hsv, upper_hsv, red=0):
    # creating mask
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
		
		# if we need to detect red we need to submerge two different masks
		# it is because hue values of red
    if red == 1:
        lower_red_l = np.array([0, 60, 20])
        upper_red_l = np.array([15, 255, 255])
        mask_l = cv2.inRange(hsv, lower_red_l, upper_red_l)
        mask = mask + mask_l
        print("red")

		#initialising mask
    bitw = cv2.bitwise_and(mask, mask, mask=mask)

    # applying opening operation
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(bitw, cv2.MORPH_OPEN, kernel)

    # removing parasites
    mask_f = ndimage.median_filter(opening, size=5)

    return mask_f
```

```python
def bounding_box(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
				# to find closest desired object we need to sort our object array
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

        while cv2.contourArea(sorted_contours[0]) > 150:
            try:
                # finding minimum enclosing circle and bounding box
                x, y, w, h = cv2.boundingRect(sorted_contours[0])
                obj_area = cv2.contourArea(sorted_contours[0])
                
                #finding radius
                radius = w / 2
                if radius < h / 2:
                    radius = h / 2

                circle_area = 3.14 * (radius ** 2)
                sf = round(obj_area / circle_area,3)

         									
								# getting center coordinates
                gX = int(x + (w / 2))
                gY = int(y + (h / 2))

								# sf filter can be usable to detect roundess of an object
								# but it wont be useful with low res. images
                # sf_check = sf > 0.4 and sf < 1.5
                
                isVertical = w/h < 1.2
                
                if isVertical == True:
                    print("object found")
                    print("object area= {}".format(obj_area))
                    print("radius= {}".format(radius))
                    print("circle area = {}".format(circle_area))
                    print("sf value = {}".format(sf)         
                    return [x, y, w, h, int(radius * 2), gX, gY, sorted_contours]
                
                else:
										# if first object don't satisfies the conditions 
							  	  # then delete object
                    print("popped")
                    sorted_contours.pop(0)
            except:
                return None

    else:
        print("none")
        return None
```

## Kullanılan HSV değerleri:

|  | Hue | Saturation | Value |
| --- | --- | --- | --- |
| lower_orange  | 0 | 103 | 170 |
| upper_orange  | 18 | 240 | 255 |
| lower_yellow  | 18 | 74 | 200 |
| upper_yellow  | 30 | 250 | 255 |

## Çıktılar:

![out_3.jpg](Robotik%20Yar%C4%B1s%CC%A7malar%C4%B1%20ic%CC%A7in%20Basit%20Nesne%20Tan%C4%B1ma%2079aa0b66af8d4466815f5a516e6d829e/out_3.jpg)

![out_4.jpg](Robotik%20Yar%C4%B1s%CC%A7malar%C4%B1%20ic%CC%A7in%20Basit%20Nesne%20Tan%C4%B1ma%2079aa0b66af8d4466815f5a516e6d829e/out_4.jpg)

![out_5.jpg](Robotik%20Yar%C4%B1s%CC%A7malar%C4%B1%20ic%CC%A7in%20Basit%20Nesne%20Tan%C4%B1ma%2079aa0b66af8d4466815f5a516e6d829e/out_5.jpg)

![out_2.jpg](Robotik%20Yar%C4%B1s%CC%A7malar%C4%B1%20ic%CC%A7in%20Basit%20Nesne%20Tan%C4%B1ma%2079aa0b66af8d4466815f5a516e6d829e/out_2.jpg)

![out_6.jpg](Robotik%20Yar%C4%B1s%CC%A7malar%C4%B1%20ic%CC%A7in%20Basit%20Nesne%20Tan%C4%B1ma%2079aa0b66af8d4466815f5a516e6d829e/out_6.jpg)

![out_1.jpg](Robotik%20Yar%C4%B1s%CC%A7malar%C4%B1%20ic%CC%A7in%20Basit%20Nesne%20Tan%C4%B1ma%2079aa0b66af8d4466815f5a516e6d829e/out_1.jpg)

## Pseudo Code:

```

img = cv2.imread(image_path)
width = img.shape[1]
height = img.shape[0]

# resizing image for faster runtime
scale_percent = 100

#cropping the sky from image
img = img [int(height/3):height,:]
height = img.shape[0]

dim = (int(width * scale_percent / 100), int(height * scale_percent / 100))
img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

#initialise masks
mask_yellow = masking(img, lower_yellow, upper_yellow, 0)
mask_orange = masking(img, lower_orange, upper_orange, 0)

#finding objects and it's features
buoy_yellow = bounding_box(mask_yellow)
buoy_orange = bounding_box(mask_orange)

# when sun reflects over an buoy, some area on orange buoy can be detected
# as yellow. So i added a filter that checks if circle of one buoy includes
# other buoy

if buoy_orange == None or buoy_yellow == None:
    pass
else:
    distance = iki dubanın merkezleri arasındaki mesafe
    radius = büyük olan dubanın çapı
    
		if distance < radius:
        if büyük çap == radius:
            küçük duba = None
        else:
            büyük duba= None

try:
    cv2.drawContours(img, buoy_yellow[7], -1, (0, 150, 150), 2)
    cv2.circle(img, (dubanın merkezi), dubanın çapı, (0, 0, 0), 2)

except:
    pass

try:
    cv2.drawContours(img, buoy_orange[7], -1, (0, 0, 255), 2)
    cv2.circle(img, (dubanın merkezi), dubanın çapı, (0, 0, 0), 2)

except:
    pass

cv2.imshow("img",img)

cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Metot 1.2 : Görüntü Sınıflandırma:

Metot 1 ile tek fark olarak bounding_box fonksiyonuna elde edilen kutuları eğittiğimiz model ile tekrar kontrol edilmesi olan bu metotta sınıflandırma için 256x256 görselleri şu model ile eğittik:

_________________________________________________________________
 Layer (type)                                               Output Shape              Param #   
==============================================================
 conv2d_13 (Conv2D)                                (None, 256, 256, 32)      832       
                                                                 
 activation_15 (Activation)                          (None, 256, 256, 32)      0         
                                                                 
 max_pooling2d_11 (MaxPooling2D)         (None, 128, 128, 32)     0                                                                  
                                                                 
 dropout_14 (Dropout)                               (None, 128, 128, 32)      0         
                                                                 
 conv2d_14 (Conv2D)                                 (None, 126, 126, 32)      9248      
                                                                 
 activation_16 (Activation)                          (None, 126, 126, 32)      0         
                                                                 
 max_pooling2d_12 (MaxPooling2D)          (None, 63, 63, 32)       0                                                                 
                                                                 
 dropout_15 (Dropout)                               (None, 63, 63, 32)        0         
                                                                 
 conv2d_15 (Conv2D)                                 (None, 61, 61, 64)        18496     
                                                                 
 activation_17 (Activation)                          (None, 61, 61, 64)        0         
                                                                 
 max_pooling2d_13 (MaxPooling2D)         (None, 30, 30, 64)       0         
                                                                                                  
 dropout_16 (Dropout)                               (None, 30, 30, 64)        0         
                                                                 
 flatten_5 (Flatten)                                      (None, 57600)             0         
                                                                 
 dense_42 (Dense)                                      (None, 64)                3686464   
                                                                 
 activation_18 (Activation)                          (None, 64)                0         
                                                                 
 dropout_17 (Dropout)                               (None, 64)                0         
                                                                 
 dense_43 (Dense)                                      (None, 1)                 65        
                                                                 
 activation_19 (Activation)                          (None, 1)                 0         
                                                                 
==============================================================
Total params: 3,715,105
Trainable params: 3,715,105
Non-trainable params: 0
_________________________________________________________________________________

test loss: 0.41632941365242004
test acc: 0.8341968655586243

![Elde edilen loss grafiği](Robotik%20Yar%C4%B1s%CC%A7malar%C4%B1%20ic%CC%A7in%20Basit%20Nesne%20Tan%C4%B1ma%2079aa0b66af8d4466815f5a516e6d829e/indir.png)

Elde edilen loss grafiği

Yaklaşık 900 resimlik bir data ile eğitilen bu modelde eğitilen görünütler siyah beyaz olmakla beraber “buoy” ve “none” olmak üzere iki sınıfa aittirler. Verilerimi güçlendirmek için uyguladığım metotta karşılaştığım hatayı giderilemediğinden dolayı validation loss minimum 0.4 seviyesine indirilebildi

Loss fonksiyonu olarak binary crossentropy kullanılırken RMSprop ile optimize edildi

İkinci konvalosyonel katmanda ve son fc katmanında aktivasyon fonksiyonu olarak ReLu yerine Sigmoid kullanıldı

Eğitimi iyileştirmek için Checkpoint, Earlystopping ve ReduceLROnPlateu fonksiyonları kullanıldı

![indir (1).png](Robotik%20Yar%C4%B1s%CC%A7malar%C4%B1%20ic%CC%A7in%20Basit%20Nesne%20Tan%C4%B1ma%2079aa0b66af8d4466815f5a516e6d829e/indir_(1).png)

tahmin: 0.00474995

![indir (2).png](Robotik%20Yar%C4%B1s%CC%A7malar%C4%B1%20ic%CC%A7in%20Basit%20Nesne%20Tan%C4%B1ma%2079aa0b66af8d4466815f5a516e6d829e/indir_(2).png)

Tahmin : 0.9429692

Sınıflandırma ikili sistem olduğu için son tek bir sınıf tahmini geri çeviren CNN modelimiz için çıktının 0’a yakınlığı duba olma ihtimalinin yüksek olduğunu gösterirken 1’e yakın olması ise duba olmama ihtimalinin yüksek olduğunu göstermektedir

### Metot 1.2 için değiştirilmiş bounding_box() fonksiyonu:

Metot 1.0’ dan farklı olarak klasik filtreleri geçtikten sonra fonksiyon istenilen değerleri vermeden önce tekrar bir “if” döngüsüne ihtiyaç duyuyoruz. Nesneyi çevreleyen kutuyu kırpıp modelden geçirdikten sonra eğer modelin çıkarttığı değer 0.5’ in altındaysa objenin değerlerini fonksiyondan çıkartırken koşul sağlanmadığı taktirde o objeyi kontür listemizden siliyoruz