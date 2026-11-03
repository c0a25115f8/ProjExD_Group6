mode = -1
submode = 0
predisp = 0
cnt = 0
max_gaze = 1000   # 最大の視線記録数
sac_x = [0 for i in range(max_gaze)]
sac_y = [0 for i in range(max_gaze)]
sac_fl = [0 for i in range(max_gaze)]

def setup():
    global mode, src, sac_x, sac_y, sac_fl,cnt
    size(1920, 1600)
    textSize(30)  
    textAlign(CENTER, CENTER)
    src = loadImage("cake.JPG")   # ファイルからの画像読み込み
    frameRate(30)

   
def draw():
    global mode, src, sac_x, sac_y,  sac_fl, cnt, submode

    threshold = 50     # サッケードと判断する最小の視線移動距離（ピクセル座標系）
    background(128)    # 背景色指定
    image(src, width/2 - src.width/2, height/2 - src.height/2)  # 画像常時

    x = mouseX
    y = mouseY
    px = pmouseX
    py = pmouseY
    # ellipse(x, y, 10, 10)
    
    if mode == 0:    

        if (0 <= x < width) and (0 <= y < height):
            d = dist(x, y, px, py)
            if d > threshold or cnt == 0:
                print("saccade " + str(cnt))
                sac_x[cnt] = x
                sac_y[cnt] = y
                sac_fl[cnt] = frameCount
                cnt += 1
                if cnt >= len(sac_x) -1:
                    mode = 1
                    print("mode " + str(mode))
        if predisp == 1:
            for i in range(1, min(cnt, 100)):
                if i > 0:
                    r = sac_fl[i] - sac_fl[i-1]
                    if r > 200:
                        r = 200
                    noFill()
                    stroke(255, 0, 0)
                    ellipse(sac_x[i], sac_y[i], r*10, r*10)
                    stroke(0, 255, 0)
                    line(sac_x[i-1], sac_y[i-1],sac_x[i], sac_y[i])
                
            for i in range(min(cnt, 100)):
                st = str(i)
                fill(0)
                text(st, sac_x[i], sac_y[i])
                fill(255)
                text(st, sac_x[i]-1, sac_y[i]-1)


    if mode == 1:
        stroke(255, 0, 0)
        for i in range(1, min(cnt, 100)):
            if i > 0:
                r = sac_fl[i] - sac_fl[i-1]
                max_fixation_range = 300    # ●最大停留円半径
                if r > max_fixation_range:
                    r = max_fixation_range
                if submode == 0:
                    # noFill()
                    stroke(255, 0, 0)
                    fill(255, 0, 0, 64)
                    ellipse(sac_x[i], sac_y[i], r*10, r*10)
                else:
                    # noStroke()
                    fill(255, 0, 0, 64)
                    ellipse(sac_x[i], sac_y[i], r*10, r*10)
                    
                stroke(0, 255, 0)
                line(sac_x[i-1], sac_y[i-1],sac_x[i], sac_y[i])
                
        for i in range(min(cnt, 100)):
            st = str(i)
            fill(0)
            text(st, sac_x[i], sac_y[i])
            fill(255)
            text(st, sac_x[i]-1, sac_y[i]-1)


def keyPressed():
    global mode, submode, predisp
    if key == " ":                         # 測定終了キー
        mode = 1
        print("mode " + str(mode))
    elif key == "s":                       # 測定開始キー
        mode = 0
        print("start")
        print(mode)
    elif key == "d":                       # 測定終了後の結果表示方法の切り替えキー
        submode = 1 - submode
    elif key == "p":                       # 測定中から視線履歴表示モードに設定するキー
        predisp = 1 -predisp