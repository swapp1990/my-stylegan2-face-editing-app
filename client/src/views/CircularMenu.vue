<template>
<div>
    <section class="menu menu--circle">
        <input type="checkbox" id="menu__active"/>
        <label for="menu__active" class="menu__active">
            <div class="menu__toggle">
            <div class="icon">
                <div class="hamburger"></div>
            </div>
            </div>
            <input type="radio" name="arrow--up" id="degree--up-0"/>
            <input type="radio" name="arrow--up" id="degree--up-1" />
            <input type="radio" name="arrow--up" id="degree--up-2" />
            <div class="menu__listings">
            <ul class="circle">
                <li>
                <div class="placeholder">
                    <div class="upside">
                    <a href="https://codepen.io/logrithumn" class="button"><i class="fa fa-user"></i></a>
                    </div>
                </div>
                </li>
                <li>
                <div class="placeholder">
                    <div class="upside">
                    <a href="#" class="button"><i class="fas fa-cog fa"></i></a>
                    </div>
                </div>
                </li>
                <li>
                <div class="placeholder">
                    <div class="upside">
                    <a href="#"><i class="fas fa-cog fa"></i></a>
                    </div>
                </div>
                </li>
                <li>
                <div class="placeholder">
                    <div class="upside">
                    <a href="#" class="button"><i class="fas fa-comments fa"></i></a>
                    </div>
                </div>
                </li>
                <li>
                <div class="placeholder">
                    <div class="upside">
                    <a href="#" class="button"><i class="fas fa-popcorn fa"></i></a>
                    </div>
                </div>
                </li>
                <li>
                <div class="placeholder">
                    <div class="upside">
                    <a href="#" class="button"><i class="fas fa-battery-half fa"></i></a>
                    </div>
                </div>
                </li>
                <li>
                <div class="placeholder">
                    <div class="upside">
                    <a href="#" class="button"><i class="fas fa-calendar fa"></i></a>
                    </div>
                </div>
                </li>
                <li>
                <div class="placeholder">
                    <div class="upside">
                    <a href="#" class="button"><i class="fas fa-cloud fa"></i></a>
                    </div>
                </div>
                </li>
                <li>
                <div class="placeholder">
                    <div class="upside">
                    <a href="#" class="button"><i class="fas fa-wifi fa"></i></a>
                    </div>
                </div>
                </li>
                <li>
                <div class="placeholder">
                    <div class="upside">
                    <a href="#" class="button"><i class="fas fa-android fa"></i></a>
                    </div>
                </div>
                </li>
            </ul>
            </div>
            <div class="menu__arrow menu__arrow--top">
                <ul>
                    <li>
                    <label for="degree--up-0"><div class="arrow"></div></label>
                    <label for="degree--up-1"><div class="arrow"></div></label>
                    <label for="degree--up-2"><div class="arrow"></div></label>
                    </li>
                </ul>
            </div>
        </label>
    </section>
</div>
</template>

<script>
    export default {
        name: "circleMenu"
    }
</script>

<style lang="stylus" scoped>
background_color = #392338
menu_color = #fff
hamburger_color = background_color
icon_hover_color = #c1264e 
arrow_hover_color = #ff947f

.icon
  position absolute
  top 70%
  left 70%
  transform translateX(-50%) translateY(-50%)

hamburger_width = 20px
hamburger_height = 2px
hamburger_animation_duration = 1s

.hamburger
  content ' '
  position relative
  width hamburger_width
  border hamburger_height solid hamburger_color
  border-radius 5px
  transition all (hamburger_animation_duration / 3) ease
  &:after, &:before
    content ' '
    position absolute
    left 50%
    width 100%
    border hamburger_height solid hamburger_color
    border-radius 5px
    transform translateX(-50%)
    transition top, bottom, transform
    transition-duration (hamburger_animation_duration / 1), (hamburger_animation_duration / 1), (hamburger_animation_duration / 4)
  &:after
    top -(hamburger_height * 4)
  &:before
    bottom -(hamburger_height * 4)
   
 
 arrow_size = 20px   
 menu_toggle_size = 200px
 menu_whole_size = menu_toggle_size * 3 + arrow_size * 2
 
 
.menu
  pointer-events none
  &--circle
    position absolute
    z-index 13
    width (menu_whole_size / 3 + arrow_size + 10)
    height (menu_whole_size / 3 + arrow_size + 10)
    background-color background_color
    overflow hidden
  &__active
    position relative
  &__toggle
    z-index 11
    position absolute
    top -(menu_toggle_size / 2)
    left -(menu_toggle_size / 2)
    width menu_toggle_size
    height menu_toggle_size
    background-color menu_color
    border-radius 50%
    transition transform (hamburger_animation_duration * 1.3)
    cursor pointer
    pointer-events auto
  &__listings
    z-index 10
    position absolute
    top -(menu_toggle_size)
    left -(menu_toggle_size)
    width (menu_toggle_size * 2)
    height (menu_toggle_size * 2)
    border-radius 50%
    transform scale(.1) rotate(150deg)
    transition transform hamburger_animation_duration 
  &__arrow
    visibility hidden
    position absolute
    input[type="radio"]
      position fixed
      top -99999px
      left -99999px
    ul
      padding 0
      margin 0
      list-style none
    &--top
      top .5em
      left (menu_toggle_size + arrow_size)
      .arrow
        transform rotate(-45deg)
    &--left
      top (menu_toggle_size + arrow_size)
      left .5em
      .arrow
        transform rotate(-135deg)
      

.arrow
  width arrow_size
  height arrow_size
  border-right (arrow_size / 3) solid menu_color
  border-top (arrow_size / 3) solid menu_color
  border-radius 3px      
  transition border-color .3s
  cursor pointer
  pointer-events auto
  &:hover
    border-color arrow_hover_color
    transition border-color .3s
        

li_count = 10
li_angle = 360 / li_count + 0deg
skew_angle =  -(90 - li_angle)
skew_angle_content = - skew_angle
li_angle_content = li_angle / 2

.circle
  position relative
  padding 0
  margin 0
  height 100%
  width 100%
  background-color menu_color
  border-radius 50%
  transform rotate(li_angle * (li_count / 2 - 2))
  overflow hidden
  list-style none
  li
    position absolute
    top 0
    right 0
    width 50%
    height 50%
    transform-origin 0 100%
    .placeholder
      position absolute
      left -100%
      padding-top 1.5em
      width 200%
      height 200%
      text-align center
      transform skewY(skew_angle_content) rotate(li_angle_content)
      .upside
        transform rotate(180deg)
      a
        text-decoration none
        pointer-events auto
      button
        pointer-events auto
      .button
        font-size 2.3em
        background-color transparent
        border none
        color background_color
        cursor pointer
    for i in (1..li_count)
      &:nth-child({i})
        transform: rotate(((i - 1) * li_angle)) skewY(skew_angle);
        background-color menu_color
        
#menu__active
  position fixed
  top -99999px
  left -99999px
  &:checked ~ label
    .menu__listings
      transform rotate(10deg) scale(1)
      transition transform hamburger_animation_duration 
    .menu__toggle
      background-color background_color
      transition all hamburger_animation_duration
    .hamburger
      border-color transparent
      transition border-color (hamburger_animation_duration / 3)
      &:after
        top -(hamburger_height)
        border-color menu_color
        transform translateX(-50%) rotate(45deg)
        transition top, transform
        transition-duration (hamburger_animation_duration / 4), hamburger_animation_duration
      &:before
        bottom -(hamburger_height)
        border-color menu_color
        transform translateX(-50%) rotate(-45deg)
        transition bottom, transform
        transition-duration (hamburger_animation_duration / 4), hamburger_animation_duration
    .button
      &:hover
        color icon_hover_color
    .menu__arrow
      visibility visible
      transition all hamburger_animation_duration (hamburger_animation_duration / .9)
    .menu__arrow--top
        label
          display none
        label[for="degree--up-0"]
          display block
    #degree--up
      &-0:checked 
        & ~ .menu__listings
          transform rotate(116deg)
        & ~ .menu__arrow--top
          label
            display none
          label[for="degree--up-1"]
            display block
      &-1:checked ~ .menu__listings
        transform rotate(224deg)
        & ~ .menu__arrow--top
          label
            display none
          label[for="degree--up-2"]
            display block
</style>