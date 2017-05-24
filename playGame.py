import pygame, sys, random, os.path, math

pygame.init()

def game(level = 1):

    # make window called screen
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Catch the butterflies...')

    # set the background
    backgroundSet =[]
    for i in range(1,5):
            namefile = os.path.join('bkg'+str(i)+'.jpg')
            bkgimage = pygame.image.load(namefile)
            backgroundSet.append(bkgimage)

    background = backgroundSet[random.randint(0,3)]
    background = pygame.transform.scale(background, (width, height))


    # load the images of the targets in the imageTarget set
    imageTarget=[]
    for i in range(1,7):
        name_of_file = os.path.join('butterfly'+str(i)+'.png')
        butterfly_image=pygame.image.load(name_of_file)
        imageTarget.append(butterfly_image)

    # load targets in an array
    targetWidth, targetHeight = 30, 30

    target_num = level * 4
    target = []
    for i in range(target_num):
        targetimage = imageTarget[random.randint(0,5)]
        targetimage = pygame.transform.scale(targetimage, (targetWidth,targetHeight))
        target.append(targetimage)

    # different speeds for every target from the array; and other variables
    gamespeed = 100
    clock = pygame.time.Clock()


    speed = []
    for i in range(target_num):
        speed.append([])
        for j in range(2):
            speed[i].append(gamespeed*random.randint(1,5))

    # set up an array targetVisible, all the targets are visible at the beginning
    targetVisible = []
    for i in range(target_num):
        targetVisible.append(True)

    # prepare the font for the game text
    gamefont = pygame.font.SysFont("comicsanms", 35)
    gamefont2 = pygame.font.SysFont("comicsanms", 25)

    # the position of every target on the screen in an array
    target_pos = []
    target_space = height/target_num - 15
    for i in range(target_num):
        target_pos.append([])
        for j in range(2):
            target_pos[i].append( i*j*target_space+50)


    # load the image player
    filename=os.path.join('net8.png')
    player = pygame.image.load(filename)
    playerWidth, playerHeight = 70, 100
    player = pygame.transform.scale(player, (playerWidth, playerHeight))
    px,py = (width-playerWidth)/2, (width-playerWidth)/2

    # prepare to show the score
    score = 0
    score_text = gamefont.render('Butterflies left to catch: ' + str(target_num-score), 1, [0,0, 0])
    boxsize = score_text.get_rect()
    scoreXpos = (width - boxsize[2]) / 2

    # prepare to show the timer
    timer = 0



    #show the level
    level_text = gamefont.render('LEVEL: '+str(level), 1, [0,0,0])

    # show the cage
    cagefile = os.path.join('cage.png')
    cage = pygame.image.load(cagefile)
    cageWidth, cageHeight = 120,150
    cage = pygame.transform.scale(cage, (cageWidth, cageHeight))
    xCage = (width - cageWidth)
    yCage =(height - cageHeight)


    # START SCREEN
    startScreen = True
    while startScreen:
        # show the background, player, cage, level and score
        screen.blit(background,(0,0))
        score_text = gamefont.render('Butterflies left to catch: ' + str(target_num - score), 1, [0,0,0])
        screen.blit(score_text, [scoreXpos, 20])
        info_text1 = gamefont2.render('You have 15 seconds to catch all the butterflies!', 1, [0,0,0])
        boxsize = info_text1.get_rect()
        info1Xpos = (width - boxsize[2]) / 2
        screen.blit(info_text1, [info1Xpos, 50])
        info_text2 = gamefont2.render('If not, all the butterflies already in the cage will be released!!', 1, [0,0,0])
        boxsize2 = info_text2.get_rect()
        info2Xpos = (width - boxsize2[2]) / 2
        screen.blit(info_text2, [info2Xpos, 80])
        screen.blit(level_text, [20, height - 50])
        screen.blit(cage, [xCage, yCage])
        screen.blit(player,(px,py))


        # show the targets
        for i in range(target_num):
            targetimage = target[i]
            x = target_pos[i][0]
            y = target_pos[i][1]
            screen.blit(targetimage, (x, y))

        # show instruction to start and play the game
        instructText = gamefont2.render('Use the mouse to catch the butterflies',1, [0,0,0])
        screen.blit(instructText, [targetWidth*5, 100])
        instructText2 = gamefont2.render('Hit the spacebar or click the mouse to start the game',1, [0,0,0])
        screen.blit(instructText2, [targetWidth *5, 160])

        pygame.display.update()

        # quiting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    startScreen = False
            elif pygame.mouse.get_pressed()[0]:
                startScreen = False

    # running the game loop
    while True:
        # show the background image, the player, the cage and the text info
        seconds = clock.tick() / 1000.0
        screen.blit(background, (0, 0))
        screen.blit(score_text, [scoreXpos, 20])
        screen.blit(level_text, [20, height - 50])
        screen.blit(cage, [xCage, yCage])
        screen.blit(player, (px, py))


        # timer increment
        seconds = clock.tick()/1000.0
        timer += seconds
        displaytimer = math.trunc(timer)

        timer_text = gamefont.render('Time: ' + str(displaytimer) + ' s', 1, [0, 0, 0])
        boxsize = timer_text.get_rect()
        timerXpos = (width - boxsize[2]) - 30
        screen.blit(timer_text, [timerXpos, 20])

        # show info about timer
        info_text = gamefont2.render('You have 15 seconds to catch all the butterflies!', 1, [0, 0, 0])
        screen.blit(info_text, [100, 50])

        # show the array of targets on the screen
        for i in range(target_num):
            targetimage = target[i]
            x = target_pos[i][0]
            y = target_pos[i][1]
            screen.blit(targetimage, (x, y))

        # for the position of the targets that are already caught should be in the cage zone
        # for the rest that are still free we should just show them
        for i in range(target_num):
            if targetVisible[i]:
                target_pos[i][0] += seconds * speed[i][0]
                target_pos[i][1] += seconds * speed[i][1]
                targetimage = target[i]
                x = target_pos[i][0]
                y = target_pos[i][1]
                screen.blit(targetimage, (x, y))

            else:
                targetimage = target[i]
                x = random.randint(xCage+20, width - targetWidth - 20)
                y = random.randint(yCage+20, height- targetHeight - 20)
                screen.blit(targetimage, (x, y))

        # tests for the borders of the screen
        for i in range(target_num):
            if target_pos[i][0] + targetWidth > width or target_pos[i][0] < 0:
                speed[i][0] = -speed[i][0]
                target_pos[i][0] += seconds * speed[i][0]
            if target_pos[i][1] > height or target_pos[i][1] < 0:
                speed[i][1] = -speed[i][1]
                target_pos[i][1] += seconds * speed[i][1]


        # mouse movements
        pygame.mouse.set_visible(0)
        pleft, ptop = pygame.mouse.get_pos()
        px, py = pleft - playerWidth / 2, ptop - playerWidth / 2

        # show the score
        score_text = gamefont.render('Butterflies left to catch: ' + str(target_num-score), 2, [0, 0, 0])
        boxsize = score_text.get_rect()
        scoreXpos = (width - boxsize[2]) / 2
        screen.blit(score_text, [scoreXpos, 20])

        # collision detection between target and player
        for i in range(target_num):
            if abs(target_pos[i][0] - px) < 15 and abs(target_pos[i][1] - py) < 15:
                target_pos[i][0] = width + 1000
                target_pos[i][1] = height + 1000
                score += 1
                targetVisible[i] = False

        # tests for timer
        if displaytimer % 15 == 0:
            for i in range(target_num):
                if targetVisible[i] == False:
                    targetVisible[i] =True
                    score=0
                    x = random.randint(xCage , width - targetWidth - 20)
                    y = random.randint(yCage , height - targetHeight - 20)
                    target_pos[i][0] = x
                    target_pos[i][1] = y
                    targetimage = target[i]
                    x = target_pos[i][0]
                    y = target_pos[i][1]
                    screen.blit(targetimage, (x, y))
        elif displaytimer == 44:
            lose_text1 = gamefont.render('You lose!!', 1, [255,255,255])
            lose_text2 = gamefont.render('It took to much time to catch them!', 1,[0, 0, 0])
            lose_text3 = gamefont.render('Go one level down and try again.', 1, [0, 0, 0])
            pygame.display.update(screen.blit(lose_text1, [100, height /2]))
            pygame.display.update(screen.blit(lose_text2, [100, height / 2+30]))
            pygame.display.update(screen.blit(lose_text3, [100, height / 2+60]))
            pygame.time.delay(2000)
            if level != 1:
                game(level-1)
            else:
                game(level)


        # show the finish of the level or the finish of the game
        if score == target_num:

            for i in range(target_num):
                if targetVisible[i] == False:
                    targetimage = target[i]
                    x = random.randint(xCage + 20, width - targetWidth - 20)
                    y = random.randint(yCage + 20, height - targetHeight - 20)
                    screen.blit(targetimage, (x, y))

            pygame.display.update()
            pygame.time.delay(1000)

            text = 'Congratulations!!  You completed this level!!'
            finish_level= gamefont.render(text, 2, [0, 0, 0])
            boxsize_finish = finish_level.get_rect()
            scoreXpos = (width - boxsize_finish[2]) / 2
            scoreYpos = (height - boxsize_finish[3]) / 2 - 100
            screen.blit(finish_level, [scoreXpos, scoreYpos])

            level += 1

            if level == 5:
                text = [None] * 5

                text[1] = ' This was the last level of the game.'
                text[2] = ' You completed the game.'
                text[3] = ' GOOD JOB!!'
                text[4] = ' The game will restart from LEVEL 1'

                finish_game = [None] * 5

                for i in range(1,5):
                    finish_game[i] = gamefont.render(text[i], 2, [0, 0, 0])
                    screen.blit(finish_game[i],[scoreXpos, scoreYpos + 100 + (i-1)*40])

                level = 1

                pygame.display.update()
                pygame.time.delay(3000)

            pygame.display.update()
            pygame.time.delay(1000)

            game(level)


        pygame.display.update()

        # quiting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()



# python's way of running the main routine
if __name__ == '__main__':
    game()