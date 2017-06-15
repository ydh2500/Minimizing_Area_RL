# Tetris by LIm
tetris made with pygame

### Tetris같은 Tetris

idea source : [tetris official](http://www.tetrisfriends.com)

<img src="./materials/image/wiki/%EC%A0%9C%EB%AA%A9%20%EC%97%86%EC%9D%8C2.png" width="350">

## 실행방법

```
python tetris.py
```
or
```
python tetris.py
```


## How to control

| Command      | Key         |
|--------------|-------------|
| Move left    | Left arrow  |
| Move right   | Right arrow |
| Rotate right | Up arrow    |
| Soft drop    | Down arrow  |
| Hard drop    | Space       |
| Hold block   | Left shift  |
| Pause game   | Esc         |
| Down faster  | press Down  |




# Base Function

1. 7개의 블럭이 랜덤으로 나와 회전키를 누르면 각자의 모양으로 회전한다.
2. 블럭이 좌우키를 누르면 좌우 한 칸씩 움직이고 블럭이 일정시간마다 한 칸씩 떨어진다.
3. 바닥에 내려가면 쌓인다.

# to Add more Function

0. game_over & hard_drop(space-bar)

 board의 가장 윗 두 줄에 닿으면, 즉   
  board의 0번째나 1번째 줄에 블럭이 존재하면
  Game_over이다.
1. start screen  
start를 누르는 게 아니라 아무 키를 누르면 시작된다.
구글의 tetris, start 이미지와 내가 만들어놓은 mino를 입체감 있게 배치했다.
start screen의 활기한 노래가 나온다.

<img src="./materials/image/wiki/%EC%A0%9C%EB%AA%A9%20%EC%97%86%EC%9D%8C2.png" width="250">


2. design
어떻게 tetris 처럼 더 만들 수 있을까?

  * add color (tetris official color)
   - Tetrimino 7개 의 색상을 맞게 구현

  * tetris board에 border draw로 격자 추가
  * 테두리에 border와 circle로 부드러운 테두리 생성
  * sound 추가
  * tetris의 아기자기하면서도 각져있는 이미지를 위해
  - [font source](http://blog.naver.com/park-yeji/220585210916)
   에서 아이럽우유라는 폰트를 적용

<img src="./materials/image/wiki/1.png" width="250">


3. functional additional things

     a. hold<Br/>
        - 블럭이 shift를 누르면 홀드할 수 있게 구현<Br/><Br/>
     b. next<Br/>
        - 다음 3번째 블럭까지 오른쪽 상단에 출력되도록 구현<Br/><Br/>
     c. score-goal-level<Br/>
        - drop, hard_drop, delete line (depends on number of lines)<Br/>
        - 각각에 따른 score가 반영되고, goal 설정에 따라 score가 goal을 넘을시 레벨이 1개씩 오름<Br/><Br/>
     d. level-speed system<Br/>
        - level을 올릴때마다 게임의 loop 속도를 올리는 방법으로 난이도를 조절<Br/><Br/>
     e. pause<Br/>
        - esc를 누르면 게임이 멈추고 다시 esc를 누르기 전까지는 pause loop가 돌아감<Br/><Br/>
     f. press down key<Br/>
        - down 방향키를 누르고 있으면 블럭이 빠르게 내려감<Br/>
        - 누르는 동안 게임 속도를 작은 값의 constance 으로 설정<Br/><Br/>
