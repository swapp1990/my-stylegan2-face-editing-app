<template>
<div class="wrapper">
    <socket-comp ref="socketComp" @gotImage="displayImage"></socket-comp>
  <div class="player__container">
    <div class="player__body">
        <div class="body__title">

        </div>
        <div class="body__box">
            <div class="imgParent" v-bind:style="{ 'background-image': imgUrl}">
                <div class="imgOverlayMenu">
                    <div></div>
                    <div>
                        <rangeslider id="menuSlider" :initVal="currAttrVal" :min="-15" :max="15" @changedAttr="onCoeffChange"></rangeslider>
                    </div>
                </div>
            </div>
            <div class="imgEdit__box">
                <ul class="list list--buttons">
                    <li v-for="attr in filteredAttr">
                        <button class="list__btn" :class="isAttrSelected(attr)" @click="changeSelectedAttr(attr)">
                            <i :class="getIcon(attr.icon)"></i>
                        </button>
                    </li>
                </ul>
            </div>
        </div>
        <div class="body__tabs">
            <ul class="list list--buttons">
                <li v-for="attrTab in attributeTabs">
                    <button class="tab__btn" :class="isAttrTabSelected(attrTab)" @click="changeSelectedTab(attrTab)">
                    <i class='fas' v-bind:class="attrTab.icon"></i></button>
                </li>
            </ul>
        </div>
      
      <div class="body__info">
        <div class="info__album">The Hunting Party</div>

        <div class="info__song">Final Masquerade</div>

        <div class="info__artist">Linkin Park</div>
      </div>

      <div class="body__buttons">
        <ul class="list list--buttons">
          <li><a href="#" class="list__link"><i class="fa fa-step-backward"></i></a></li>

          <li><a href="#" class="list__link"><i class="fa fa-play"></i></a></li>

          <li><a href="#" class="list__link"><i class="fa fa-step-forward"></i></a></li>
        </ul>
      </div>
    </div>

    <div class="player__footer">
      <ul class="list list--footer">
        <li><a href="#" class="list__link"><i class="fa fa-heart-o"></i></a></li>
        
        <li><a href="#" class="list__link"><i class="fa fa-random"></i></a></li>
        
        <li><a href="#" class="list__link"><i class="fa fa-undo"></i></a></li>
        
        <li><a href="#" class="list__link"><i class="fa fa-ellipsis-h"></i></a></li>
      </ul>
    </div>
  </div>
</div>
</template>

<script>
import logoHeading from '@/components/LogoHeading.vue';
import neubox from '@/components/NeuBox.vue';
import rangeslider from '@/components/RangeSlider.vue';
import socketComp from '@/components/Socket.vue';
    export default {
        name: "homenew",
        components: {
            logoHeading: logoHeading,
            neubox: neubox,
            rangeslider: rangeslider,
            socketComp: socketComp
        },
        data() {
            return {
                imgUrl: "",
                //face editing
                attributeTabs: [
                    {name: 'basic', icon: 'fa-dna'},
                    {name: 'emotion', icon: 'fa-grin-beam'},
                    {name: 'structure', icon: 'fa-hammer'}
                ],
                selectedAttrTab: 'basic',
                filteredAttr: [],
                currAttrVal: 0,
                attributes: [
                    {name: 'smile', coeff: 0.0, tabTag: 'basic', icon: 'far fa-smile'}, 
                    {name: 'gender', coeff: 0.0, tabTag: 'basic', icon:'fas fa-venus-mars'},
                    {name: 'age', coeff: 0.0, tabTag: 'basic', icon:'fas fa-child'},
                    {name: 'beauty', coeff: 0.0},
                    {name: 'glasses', coeff: 0.0},
                    {name: 'race_black', coeff: 0.0, tabTag: 'basic', icon:'fas fa-globe-africa'},
                    {name: 'race_yellow', coeff: 0.0, tabTag: 'basic', icon:'fas fa-globe-asia'},
                    {name: 'emotion_fear', coeff: 0.0, tabTag: 'emotion', icon:'fas fa-ghost'},
                    {name: 'emotion_angry', coeff: 0.0, tabTag: 'emotion', icon:'far fa-angry'},
                    {name: 'emotion_disgust', coeff: 0.0, tabTag: 'emotion', icon:'far fa-tired'},
                    {name: 'emotion_easy', coeff: 0.0, tabTag: 'emotion', icon:'fas fa-couch'},
                    {name: 'eyes_open', coeff: 0.0, tabTag: 'structure', icon:'fas fa-eye'},
                    {name: 'angle_horizontal', coeff: 0.0, tabTag: 'structure', icon:'fas fa-arrows-alt-h'},
                    {name: 'angle_pitch', coeff: 0.0, tabTag: 'structure', icon:'fas fa-arrows-alt-v'},
                    {name: 'face_shape', coeff: 0.0, tabTag: 'structure', icon:'fas fa-weight'},
                    {name: 'height', coeff: 0.0, tabTag: 'structure', icon:'fas fa-text-height'},
                    {name: 'width', coeff: 0.0, tabTag: 'structure', icon:'fas fa-text-width'},
                ],
                currSelectedAttr: null,
            }
        },
        mounted() {
            this.loadDefaultImg();
            this.calculateFilteredAttr();
        },
        methods: {
            loadDefaultImg() {
                var img = 'url("./resImg.jpg")';
                this.imgUrl = img;
            },
            displayImage(imgData) {
                this.imgUrl = imgData.imgUrl;
            },
            getTabClass(attrTab) {
                if(attrTab.name === this.selectedAttrTab) {
                    return "attrTabSelected";
                }
                return "attrTab";
            },
            getIcon(iconClass) {
                return iconClass + " fa-lg fa-fw";
            },
            reset() {

            },
            calculateFilteredAttr() {
                this.filteredAttr = this.attributes.filter(a => {
                    return a.tabTag === this.selectedAttrTab;
                });
                this.currSelectedAttr = this.filteredAttr[0];
            },
            isAttrSelected(attr) {
                if(attr.name === this.currSelectedAttr.name) {
                    return "isSelected";
                }
                return ""
            },
            isAttrTabSelected(attrTab) {
                if(attrTab.name === this.selectedAttrTab) {
                    return "isSelected";
                }
                return ""
            },
            changeSelectedAttr(attr) {
                this.currSelectedAttr = attr;
                this.currAttrVal = Number(this.currSelectedAttr.coeff);
            },
           changeSelectedTab(attrTab) {
                this.selectedAttrTab = attrTab.name;
                this.calculateFilteredAttr();
            },
            onCoeffChange(coeff) {
                // console.log("coeff ", coeff);
                this.currSelectedAttr.coeff = coeff;
                this.currAttrVal = Number(coeff);
                let params = this.currSelectedAttr;
                this.$refs.socketComp.sendEditAction("changeCoeff", params);
            }
        }
    }
</script>

<style lang="scss" scoped>
// Functions
@function remy($value, $base: 16px) {
  @return ($value / $base) * 1rem;
}

// Mixins
@mixin transition($prop: all, $duration: .25s, $timing: cubic-bezier(.4, 0, 1, 1)) {
  transition: $prop $duration $timing;
}

// Colors
$color-black: #212121;
$color-blue: #03a9f4;
$color-red: #d30320;
$color-bg: #f5f6f7;


// Variables
$boxshadow-0: 0 1px 3px -5px rgba(0, 0, 0, .13),
0 1px 3px -10px rgba(0, 0, 0, .23);
$boxshadow-1: 0 3px 6px -5px rgba(0, 0, 0, .16),
0 3px 6px -10px rgba(0, 0, 0, .23);
$boxshadow-2: 0 10px 20px -5px rgba(0, 0, 0, .19),
0 6px 6px -10px rgba(0, 0, 0, .23);
$boxshadow-3: 0 14px 28px -5px rgba(0, 0, 0, .25),
0 10px 10px -10px rgba(0, 0, 0, .22);
$radius: remy(4px);

$white: #ffffff;
$dark: rgba(52, 55, 61, 0.6);

.player__container {
    margin: 0 auto;
    max-width: 100%;
    background: #E0E5EC;
    border-radius: $radius;
    box-shadow: $boxshadow-2;

    //Center the box to the screen
    // display: flex;
    // align-items: center;
    // justify-content: center;
    justify-content: space-between;
}
%neuBox {
background-color: #f5f6f7;
border-radius: $radius;
box-shadow: -4px -2px 4px 0px  $white, 4px 2px 6px 0px $dark;
margin: 0 auto;
}
.body__box {
    @extend %neuBox;
    max-width: 640px;
    height: 620px;
    @media only screen and (max-width: 640px) {
        margin-left: 10px;
        margin-right: 10px;
    }
    z-index: 3;
}
.imgParent {
    position: relative;
    margin: 0 auto;
    @media only screen and (max-width: 640px) {
        width: 95%;
    }
    margin-bottom: 5px;
    width: 100%;
    height: 512px;
    background-repeat: no-repeat;
    background-size: auto;
    background-position: center;
    z-index: 1;
}
.imgOverlayMenu {
    display: grid;
    height: inherit;
    grid-template-rows: 5fr 1fr;
    grid-template-columns: auto;
    align-items: end;
}
.body__title {
    @extend %neuBox;
    max-width: 640px;
    height: 100px;
    @media only screen and (max-width: 640px) {
        height: 10px;
    }
}
.imgEdit__box {
    @extend %neuBox;
    z-index: 2;
    max-width: 640px;
    height: 90px;
    //content
    display: flex;
    justify-content: center;
}
.body__tabs {
    display: flex;
    height: 100px;
    z-index: 1;
}
%neuBtn {
    color: inherit;
    position: relative;
    background: inherit;
    outline: none;
    border: none;
    border-radius: $radius;
    box-shadow: -4px -2px 4px 0px  $white, 4px 2px 6px 0px $dark;
}
.list {
    margin: 0;
    padding: 0;
    list-style-type: none;
    &.list--buttons {
        display: flex;
        align-items: center;
        justify-content: space-around;
        flex-grow: 1;
        flex-basis: 20%;
    }
}
.list__btn {
    @extend %neuBtn;
    width: 40px;
    height: 40px;
    &:hover {
        color: darken(rgba($color-red, .95), 8%);
        opacity: 1;
    }
    // &:focus {
    //     color: darken(rgba($color-red, .95), 8%);
    //     box-shadow: 0px 0px 1px 1px $white inset, 2px 2px 2px 0px $dark inset;
    // }
    &.isSelected {
        color: darken(rgba($color-red, .95), 8%);
        box-shadow: 0px 0px 1px 1px $white inset, 2px 2px 2px 0px $dark inset;
    }
}
.tab__btn {
    @extend %neuBtn;
    background-color: #f5f6f7;
    position: relative;
    top: -10px;
    width: 60px;
    height: 80px;
    padding: 0;
    &:hover {
        color: darken(rgba($color-red, .95), 8%);
        opacity: 1;
    }
    &.isSelected {
        color: darken(rgba($color-red, .95), 8%);
        box-shadow: 0px 0px 1px 1px $white inset, 2px 2px 2px 0px $dark inset;
    }
}

.body__cover {
  position: relative;
}

.body__cover img {
  max-width: 100%;
  border-radius: $radius;
}

.body__buttons,
.body__info,
.player__footer {
  padding-right: 2rem;
  padding-left: 2rem;
}

.list--cover,
.list--footer {
  justify-content: space-between;
}

.list--header .list__link,
.list--footer .list__link {
  color: #888;
}

.list--cover {
  position: absolute;
  top: .5rem;
  width: 100%;

  li:first-of-type {
    margin-left: .75rem;
  }

  li:last-of-type {
    margin-right: .75rem;
  }

  a {
    font-size: 1.15rem;
    color: #fff;
  }
}

.range {
  position: relative;
  top: -1.5rem;
  right: 0;
  left: 0;
  margin: auto;
  background: rgba(#fff, .95);
  width: 80%;
  height: remy(2px);
  border-radius: $radius;
  cursor: pointer;

  &:before,
  &:after {
    content: "";
    position: absolute;
    cursor: pointer;
  }

  &:before {
    width: 3rem;
    height: 100%;
    background: linear-gradient(to right, rgba($color-red, .5), rgba($color-red, .85));
    border-radius: $radius;
    overflow: hidden;
  }

  &:after {
    top: remy(-6px);
    left: 3rem;
    z-index: 3;
    width: remy(14px);
    height: remy(14px);
    background: #fff;
    border-radius: 50%;
    box-shadow: 0 0 3px rgba(0, 0, 0, .15), 0 2px 4px rgba(0, 0, 0, .15);
    
    @include transition;
  }
  
  &:focus,
  &:hover {
    &:after {
      background: rgba($color-red, .95);
    }
  }
}

.body__info {
  padding-top: 1.5rem;
  padding-bottom: 1.25rem;
  text-align: center;
}

.info__album,
.info__song {
  margin-bottom: .5rem;
}

.info__artist,
.info__album {
  font-size: .75rem;
  font-weight: 300;
  color: #666;
}

.info__song {
  font-size: 1.15rem;
  font-weight: 400;
  color: $color-red;
}

.body__buttons {
  padding-bottom: 2rem;
}

.body__buttons {
  padding-top: 1rem;
}


// .list--buttons li:nth-of-type(n+2) {
//   margin-left: 1.25rem;
// }

// .list--buttons a {
//   padding-top: .45rem;
//   padding-right: .75rem;
//   padding-bottom: .45rem;
//   padding-left: .75rem;
//   font-size: 1rem;
//   border-radius: 50%;
//   box-shadow: 0 3px 6px rgba(33,33,33,.1), 0 3px 12px rgba(33,33,33,.15);

//   &:focus,
//   &:hover {
//     color: darken(rgba($color-red, .95), 8%);
//     opacity: 1;
//     box-shadow: 0 6px 9px rgba(33,33,33,.1), 0 6px 16px rgba(33,33,33,.15);
//   }
// }

// .list--buttons li:nth-of-type(2) a {
//   padding-top: .82rem;
//   padding-right: 1rem;
//   padding-bottom: .82rem;
//   padding-left: 1.19rem;
//   margin-left: .5rem;
//   font-size: 1.25rem;
//   color: rgba($color-red, .95);
// }

// .list--buttons li:first-of-type a,
// .list--buttons li:last-of-type a {
//   font-size: .95rem;
//   color: #212121;
//   opacity: .5;

//   &:focus,
//   &:hover {
//     color: $color-red;
//     opacity: .75;
//   }
// }

// .list__link {
//   @include transition;

//   &:focus,
//   &:hover {
//     color: $color-red;
//   }
// }

.player__footer {
  padding-top: 1rem;
  padding-bottom: 2rem;
}

.list--footer a {
  opacity: .5;

  &:focus,
  &:hover {
    opacity: .9;
  }
}

</style>