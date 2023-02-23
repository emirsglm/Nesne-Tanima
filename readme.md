\hypertarget{robotik-yarux131ux15fmalarux131-iuxe7in-basit-nesne-tanux131ma}{%
\section{Robotik Yarışmaları için Basit Nesne
Tanıma}\label{robotik-yarux131ux15fmalarux131-iuxe7in-basit-nesne-tanux131ma}}

\hypertarget{e1f622ff-6588-439d-85da-30608fa85d27}{%
\subsection{Projenin temel
hedefleri:}\label{e1f622ff-6588-439d-85da-30608fa85d27}}

\begin{itemize}
\tightlist
\item
  Düşük donanımlı sistemlerde çalışmalı
\end{itemize}

\begin{itemize}
\tightlist
\item
  Gerçek zamanlı görüntü işleyebilmeli
\end{itemize}

\hypertarget{d30b60c2-0b3a-4038-94ab-316ee2c0e51b}{%
\section{Yaklaşım:}\label{d30b60c2-0b3a-4038-94ab-316ee2c0e51b}}

Renk özelliğini kullanarak nesne tanıma

Robotik yarışmalarında hedefler genellikle renk değerleriyle öne çıkan
hedefler olduğu için nesne tespitinde renk özelliğin kullanarak
maskeleme yapmak en kolay yaklaşım olacaktır.

\textbf{HSV:}

HSV objenin hue, saturation ve value değerlerini gösteren bir renk şema
sistemidir. HSV renk şemasında ortam ışığına bağlı olarak sadece
saturation ve value değerlerinde farklılık gösterdiği için renk
özelliğinde maskeleme yapmak için kullanımı daha verimli olacaktır.

Alt ve üst sınırlarını belirlediğimiz hsv değerleri maskelememizin ilk
adımını oluşturur

\textbf{Opening}:

Elde ettiğimiz maskede aslında ayrık olan alanlar ufak değerlerle
birbiri ile birleşik gözükebilmektedir. Böyle nesneleri biribirinden
ayırmak için erozyon ve korozyon operasyonlarını art arda kullanan
opening fonksiyonunu kullanmak nesnelerin ayrılmasını sağlayacaktır

\textbf{Median Filter:}

Maskeleme ve opening operasyonlarının ardından maskeyi parazitlerden
arındırmak şekillerin kenar çizgilerini bulmayı kolaylaştırmaktadır.

Elde edilen maskede görevin gerekliliklerine göre çeşitli filtrelemeler
kullanılabilir. Örneğin duba tespit etmek için alanların yuvarlaklığı
kıyaslanabilir. Çoğu görevde olabilecek ortak bir filtreleme ise
nesnenin alan büyüklüğü olabilir. Görev esnasında kameraya en yakın
obje, tespit etmek istenilen obje ise algılanan alanlar arasında en
büyükleri üzerinden işlem yapmak işlem süresini kısaltır.

Renk özelliğinden yola çıkarak elde edilen ROI'leri algoritmanın
doğruluk açısından güçlendirilmesi için bir katman daha filtreleme
eklenebilir

Şekil özelliğini kullanarak filtreleme

Renk değerlerini alınan obje özel bir reflektör renge boyanmadıysa
ortamın ışıklandırmasından dolayı objenin şekliyle birebir
uyuşmayabilir. Bundan dolayı ilk katman filtrelemeden elde edilen alana
gerçek resim üzerinden şekil özelliğini değerlendiren bir katman
eklenebilir

\begin{itemize}
\item
  Canny edge detector:

  Aşağıdaki 5 adımdan oluşan canny edge detector ile ROI içindeki nesne
  yuvarlaklığı üzerinden değerlendirilebilir

  \begin{enumerate}
  \def\labelenumi{\arabic{enumi}.}
  \tightlist
  \item
    Gaussian filtre ile görüntüyü yumuşatma
  \end{enumerate}

  \begin{enumerate}
  \def\labelenumi{\arabic{enumi}.}
  \setcounter{enumi}{1}
  \tightlist
  \item
    Resmin gradyan yoğunluğunu hesaplama (bkz. sobel operator)
  \end{enumerate}

  \begin{enumerate}
  \def\labelenumi{\arabic{enumi}.}
  \setcounter{enumi}{2}
  \tightlist
  \item
    NMS ile yanlış kenarları silme
  \end{enumerate}

  \begin{enumerate}
  \def\labelenumi{\arabic{enumi}.}
  \setcounter{enumi}{3}
  \tightlist
  \item
    Gradyan yoğunluğunu treshold ile alt ve üst sınırlarını belirleyerek
    filtreleme
  \end{enumerate}

  \begin{enumerate}
  \def\labelenumi{\arabic{enumi}.}
  \setcounter{enumi}{4}
  \tightlist
  \item
    Hysteresis kullanarak güçlü kenarlara bağlanmayan zayıf kenarları
    silme
  \end{enumerate}
\end{itemize}

CNN kullanarak

\begin{itemize}
\item
  Siyah Beyaz model eğitimi*

  Bir görsel sınıflandırma modeli eğiterek belirlenen ROI'lerin duba
  barındırıp barındırmadığı tespit edilebilir

  ROI'ler renklerden tespit edildiği için renkli görüntü kullanılması
  yerine daha küçük bir modelin kullanılabilmesini sağlamak için veri
  setinde siyah beyaz görüntü kullanılabilir.
\end{itemize}

\begin{itemize}
\item
  Binary görsel model eğitimi

  Siyah Beyaz yerine modelimizi binary görüntülerden oluşan bir veri
  seti eğitilip performansları karşılaştırılabilir
\end{itemize}

CNN ile nesne tanıma

Performans açısından donanıma ve göreve uygun olarak mobil CNN modelleri
kullanarak nesne tespiti yapılabilir. Hız açısından daha hızlı ama
doğruluğu daha az modeller tercih edilebileceği gibi daha yavaş ama daha
doğru modelleri hızlandırmak da tercih edilebilir.

Modelimizin hızını arttırmak için :

\begin{itemize}
\tightlist
\item
  Tek cisim ise:

  \begin{itemize}
  \tightlist
  \item
    Siyah beyaz model eğitilebilir
  \end{itemize}

  \begin{itemize}
  \tightlist
  \item
    Renk özelliklerini kullanarak uyguladığımız filtrelemeyi yapıp
    buradan veri seti oluşturarak binary görüntüden model eğitilebilir
  \end{itemize}
\end{itemize}

\begin{itemize}
\tightlist
\item
  Birden çok cisim ise

  \begin{itemize}
  \tightlist
  \item
    Siyah beyaz model eğitilebilir. Nesneyi tespit ettikten sonra elde
    ettiğimiz çerçeve içindeki rengi algılayabiliriz
  \end{itemize}
\end{itemize}

\hypertarget{a71024de-e464-4bb7-b3ab-f252ec53f8e7}{%
\section{Metot 1.0 : Renk
özellikleri}\label{a71024de-e464-4bb7-b3ab-f252ec53f8e7}}

Kullanılan Fonksiyonlar

\hypertarget{3111a63a-81b3-454d-a287-60b1887282c2}{%
\label{3111a63a-81b3-454d-a287-60b1887282c2}}%
\begin{Shaded}
\begin{Highlighting}[]
\NormalTok{def masking(img, lower\_hsv, upper\_hsv, red=0):}
\NormalTok{    \# creating mask}
\NormalTok{    hsv = cv2.cvtColor(img, cv2.COLOR\_BGR2HSV)}
\NormalTok{    mask = cv2.inRange(hsv, lower\_hsv, upper\_hsv)}
        
\NormalTok{        \# if we need to detect red we need to submerge two different masks}
\NormalTok{        \# it is because hue values of red}
\NormalTok{    if red == 1:}
\NormalTok{        lower\_red\_l = np.array([0, 60, 20])}
\NormalTok{        upper\_red\_l = np.array([15, 255, 255])}
\NormalTok{        mask\_l = cv2.inRange(hsv, lower\_red\_l, upper\_red\_l)}
\NormalTok{        mask = mask + mask\_l}
\NormalTok{        print("red")}

\NormalTok{        \#initialising mask}
\NormalTok{    bitw = cv2.bitwise\_and(mask, mask, mask=mask)}

\NormalTok{    \# applying opening operation}
\NormalTok{    kernel = np.ones((3, 3), np.uint8)}
\NormalTok{    opening = cv2.morphologyEx(bitw, cv2.MORPH\_OPEN, kernel)}

\NormalTok{    \# removing parasites}
\NormalTok{    mask\_f = ndimage.median\_filter(opening, size=5)}

\NormalTok{    return mask\_f}
\end{Highlighting}
\end{Shaded}

\hypertarget{e3aca0fe-6670-4178-98f0-b7e52f34a682}{%
\label{e3aca0fe-6670-4178-98f0-b7e52f34a682}}%
\begin{Shaded}
\begin{Highlighting}[]
\NormalTok{def bounding\_box(mask):}
\NormalTok{    contours, \_ = cv2.findContours(mask, cv2.RETR\_EXTERNAL, cv2.CHAIN\_APPROX\_NONE)}

\NormalTok{    if len(contours) \textgreater{} 0:}
\NormalTok{                \# to find closest desired object we need to sort our object array}
\NormalTok{        sorted\_contours = sorted(contours, key=cv2.contourArea, reverse=True)}

\NormalTok{        while cv2.contourArea(sorted\_contours[0]) \textgreater{} 150:}
\NormalTok{            try:}
\NormalTok{                \# finding minimum enclosing circle and bounding box}
\NormalTok{                x, y, w, h = cv2.boundingRect(sorted\_contours[0])}
\NormalTok{                obj\_area = cv2.contourArea(sorted\_contours[0])}
                
\NormalTok{                \#finding radius}
\NormalTok{                radius = w / 2}
\NormalTok{                if radius \textless{} h / 2:}
\NormalTok{                    radius = h / 2}

\NormalTok{                circle\_area = 3.14 * (radius ** 2)}
\NormalTok{                sf = round(obj\_area / circle\_area,3)}

                                            
\NormalTok{                                \# getting center coordinates}
\NormalTok{                gX = int(x + (w / 2))}
\NormalTok{                gY = int(y + (h / 2))}

\NormalTok{                                \# sf filter can be usable to detect roundess of an object}
\NormalTok{                                \# but it wont be useful with low res. images}
\NormalTok{                \# sf\_check = sf \textgreater{} 0.4 and sf \textless{} 1.5}
                
\NormalTok{                isVertical = w/h \textless{} 1.2}
                
\NormalTok{                if isVertical == True:}
\NormalTok{                    print("object found")}
\NormalTok{                    print("object area= \{\}".format(obj\_area))}
\NormalTok{                    print("radius= \{\}".format(radius))}
\NormalTok{                    print("circle area = \{\}".format(circle\_area))}
\NormalTok{                    print("sf value = \{\}".format(sf)         }
\NormalTok{                    return [x, y, w, h, int(radius * 2), gX, gY, sorted\_contours]}
                
\NormalTok{                else:}
\NormalTok{                                        \# if first object don\textquotesingle{}t satisfies the conditions }
\NormalTok{                                  \# then delete object}
\NormalTok{                    print("popped")}
\NormalTok{                    sorted\_contours.pop(0)}
\NormalTok{            except:}
\NormalTok{                return None}

\NormalTok{    else:}
\NormalTok{        print("none")}
\NormalTok{        return None}
\end{Highlighting}
\end{Shaded}

\hypertarget{41351d7e-0395-4759-ae35-15c19f368625}{%
\subsection{Kullanılan HSV
değerleri:}\label{41351d7e-0395-4759-ae35-15c19f368625}}

\begin{longtable}[]{@{}llll@{}}
\toprule
& Hue & Saturation & Value \\
\midrule
\endhead
lower\_orange & 0 & 103 & 170 \\
upper\_orange & 18 & 240 & 255 \\
lower\_yellow & 18 & 74 & 200 \\
upper\_yellow & 30 & 250 & 255 \\
\bottomrule
\end{longtable}

\hypertarget{049bf1de-3941-472d-95ea-f109b3d574d7}{%
\subsection{Çıktılar:}\label{049bf1de-3941-472d-95ea-f109b3d574d7}}

\hypertarget{d1a32830-7d74-49e7-8f28-3764a39d8719}{}
\leavevmode\vadjust pre{\hypertarget{9727b28f-367b-4315-b6cf-7b6955b3e598}{}}%
\begin{figure}
\centering
\includegraphics{Robotik Yarışmaları için Basit Nesne Tanıma 79aa0b66af8d4466815f5a516e6d829e/out_3.jpg}
\caption{}
\end{figure}

\leavevmode\vadjust pre{\hypertarget{33fa3e36-5689-4eb0-bc90-7226157d9ad7}{}}%
\begin{figure}
\centering
\includegraphics{Robotik Yarışmaları için Basit Nesne Tanıma 79aa0b66af8d4466815f5a516e6d829e/out_4.jpg}
\caption{}
\end{figure}

\leavevmode\vadjust pre{\hypertarget{2642f30d-8c41-4057-9a5d-62fd80a106ea}{}}%
\begin{figure}
\centering
\includegraphics{Robotik Yarışmaları için Basit Nesne Tanıma 79aa0b66af8d4466815f5a516e6d829e/out_5.jpg}
\caption{}
\end{figure}

\hypertarget{e94f855e-2e7c-4f99-ad3a-c01beb442f2e}{}
\leavevmode\vadjust pre{\hypertarget{830367de-97c0-47c6-ac33-6c4991104900}{}}%
\begin{figure}
\centering
\includegraphics{Robotik Yarışmaları için Basit Nesne Tanıma 79aa0b66af8d4466815f5a516e6d829e/out_2.jpg}
\caption{}
\end{figure}

\leavevmode\vadjust pre{\hypertarget{510a2af8-5518-4f35-8b8e-2e91ac916afe}{}}%
\begin{figure}
\centering
\includegraphics{Robotik Yarışmaları için Basit Nesne Tanıma 79aa0b66af8d4466815f5a516e6d829e/out_6.jpg}
\caption{}
\end{figure}

\leavevmode\vadjust pre{\hypertarget{b0da36c3-cc19-4291-84a2-47cb1262e549}{}}%
\begin{figure}
\centering
\includegraphics{Robotik Yarışmaları için Basit Nesne Tanıma 79aa0b66af8d4466815f5a516e6d829e/out_1.jpg}
\caption{}
\end{figure}

\hypertarget{2e5cdef9-4474-4f72-9020-eb6c41bc77e1}{%
\subsection{Pseudo Code:}\label{2e5cdef9-4474-4f72-9020-eb6c41bc77e1}}

\hypertarget{9260d786-dcc1-4992-bb32-356864200153}{%
\label{9260d786-dcc1-4992-bb32-356864200153}}%
\begin{Shaded}
\begin{Highlighting}[]
\NormalTok{img = cv2.imread(image\_path)}
\NormalTok{width = img.shape[1]}
\NormalTok{height = img.shape[0]}

\NormalTok{\# resizing image for faster runtime}
\NormalTok{scale\_percent = 100}

\NormalTok{\#cropping the sky from image}
\NormalTok{img = img [int(height/3):height,:]}
\NormalTok{height = img.shape[0]}

\NormalTok{dim = (int(width * scale\_percent / 100), int(height * scale\_percent / 100))}
\NormalTok{img = cv2.resize(img, dim, interpolation=cv2.INTER\_AREA)}

\NormalTok{\#initialise masks}
\NormalTok{mask\_yellow = masking(img, lower\_yellow, upper\_yellow, 0)}
\NormalTok{mask\_orange = masking(img, lower\_orange, upper\_orange, 0)}

\NormalTok{\#finding objects and it\textquotesingle{}s features}
\NormalTok{buoy\_yellow = bounding\_box(mask\_yellow)}
\NormalTok{buoy\_orange = bounding\_box(mask\_orange)}

\NormalTok{\# when sun reflects over an buoy, some area on orange buoy can be detected}
\NormalTok{\# as yellow. So i added a filter that checks if circle of one buoy includes}
\NormalTok{\# other buoy}

\NormalTok{if buoy\_orange == None or buoy\_yellow == None:}
\NormalTok{    pass}
\NormalTok{else:}
\NormalTok{    distance = iki dubanın merkezleri arasındaki mesafe}
\NormalTok{    radius = büyük olan dubanın çapı}
    
\NormalTok{        if distance \textless{} radius:}
\NormalTok{        if büyük çap == radius:}
\NormalTok{            küçük duba = None}
\NormalTok{        else:}
\NormalTok{            büyük duba= None}


\NormalTok{try:}
\NormalTok{    cv2.drawContours(img, buoy\_yellow[7], {-}1, (0, 150, 150), 2)}
\NormalTok{    cv2.circle(img, (dubanın merkezi), dubanın çapı, (0, 0, 0), 2)}

\NormalTok{except:}
\NormalTok{    pass}

\NormalTok{try:}
\NormalTok{    cv2.drawContours(img, buoy\_orange[7], {-}1, (0, 0, 255), 2)}
\NormalTok{    cv2.circle(img, (dubanın merkezi), dubanın çapı, (0, 0, 0), 2)}

\NormalTok{except:}
\NormalTok{    pass}

\NormalTok{cv2.imshow("img",img)}

\NormalTok{cv2.waitKey(0)}
\NormalTok{cv2.destroyAllWindows()}
\end{Highlighting}
\end{Shaded}

\hypertarget{99aac3de-b2c8-4a76-9b15-65ed747fa1f4}{%
\subsection{Metot 1.2 : Görüntü
Sınıflandırma:}\label{99aac3de-b2c8-4a76-9b15-65ed747fa1f4}}

Metot 1 ile tek fark olarak bounding\_box fonksiyonuna elde edilen
kutuları eğittiğimiz model ile tekrar kontrol edilmesi olan bu metotta
sınıflandırma için 256x256 görselleri şu model ile eğittik:

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
Layer (type) Output Shape Param \#
==============================================================
conv2d\_13 (Conv2D) (None, 256, 256, 32) 832 activation\_15 (Activation)
(None, 256, 256, 32) 0 max\_pooling2d\_11 (MaxPooling2D) (None, 128,
128, 32) 0 dropout\_14 (Dropout) (None, 128, 128, 32) 0 conv2d\_14
(Conv2D) (None, 126, 126, 32) 9248 activation\_16 (Activation) (None,
126, 126, 32) 0 max\_pooling2d\_12 (MaxPooling2D) (None, 63, 63, 32) 0
dropout\_15 (Dropout) (None, 63, 63, 32) 0 conv2d\_15 (Conv2D) (None,
61, 61, 64) 18496 activation\_17 (Activation) (None, 61, 61, 64) 0
max\_pooling2d\_13 (MaxPooling2D) (None, 30, 30, 64) 0 dropout\_16
(Dropout) (None, 30, 30, 64) 0 flatten\_5 (Flatten) (None, 57600) 0
dense\_42 (Dense) (None, 64) 3686464 activation\_18 (Activation) (None,
64) 0 dropout\_17 (Dropout) (None, 64) 0 dense\_43 (Dense) (None, 1) 65
activation\_19 (Activation) (None, 1) 0
============================================================== Total
params: 3,715,105 Trainable params: 3,715,105 Non-trainable params: 0
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

test loss: 0.41632941365242004 test acc: 0.8341968655586243

\begin{figure}
\centering
\includegraphics{Robotik Yarışmaları için Basit Nesne Tanıma 79aa0b66af8d4466815f5a516e6d829e/indir.png}
\caption{Elde edilen loss grafiği}
\end{figure}

Yaklaşık 900 resimlik bir data ile eğitilen bu modelde eğitilen
görünütler siyah beyaz olmakla beraber ``buoy'' ve ``none'' olmak üzere
iki sınıfa aittirler. Verilerimi güçlendirmek için uyguladığım metotta
karşılaştığım hatayı giderilemediğinden dolayı validation loss minimum
0.4 seviyesine indirilebildi

Loss fonksiyonu olarak binary crossentropy kullanılırken RMSprop ile
optimize edildi

İkinci konvalosyonel katmanda ve son fc katmanında aktivasyon fonksiyonu
olarak ReLu yerine Sigmoid kullanıldı

Eğitimi iyileştirmek için Checkpoint, Earlystopping ve ReduceLROnPlateu
fonksiyonları kullanıldı

\hypertarget{9d92fa77-7fad-4d41-b508-2b393d3222f0}{}
\leavevmode\vadjust pre{\hypertarget{100484bd-8d0b-41a5-99b8-1117585de3fb}{}}%
\begin{figure}
\centering
\includegraphics{Robotik Yarışmaları için Basit Nesne Tanıma 79aa0b66af8d4466815f5a516e6d829e/indir_(1).png}
\caption{}
\end{figure}

tahmin: 0.00474995

\leavevmode\vadjust pre{\hypertarget{96e8b4fb-e86e-4f3d-9f11-5f3a2f608a48}{}}%
\begin{figure}
\centering
\includegraphics{Robotik Yarışmaları için Basit Nesne Tanıma 79aa0b66af8d4466815f5a516e6d829e/indir_(2).png}
\caption{}
\end{figure}

Tahmin : 0.9429692

Sınıflandırma ikili sistem olduğu için son tek bir sınıf tahmini geri
çeviren CNN modelimiz için çıktının 0'a yakınlığı duba olma ihtimalinin
yüksek olduğunu gösterirken 1'e yakın olması ise duba olmama ihtimalinin
yüksek olduğunu göstermektedir

\hypertarget{960106eb-a31d-405d-acaa-fdcb8a0d6859}{%
\subsubsection{Metot 1.2 için değiştirilmiş bounding\_box()
fonksiyonu:}\label{960106eb-a31d-405d-acaa-fdcb8a0d6859}}

Metot 1.0' dan farklı olarak klasik filtreleri geçtikten sonra fonksiyon
istenilen değerleri vermeden önce tekrar bir ``if'' döngüsüne ihtiyaç
duyuyoruz. Nesneyi çevreleyen kutuyu kırpıp modelden geçirdikten sonra
eğer modelin çıkarttığı değer 0.5' in altındaysa objenin değerlerini
fonksiyondan çıkartırken koşul sağlanmadığı taktirde o objeyi kontür
listemizden siliyoruz
