<template>
<div class="wrapper">
    <div class="main-head"><logoHeading></logoHeading></div>
    <!-- <nav class="main-nav">
        <ul>
            <li><a href="">Nav 1</a></li>
            <li><a href="">Nav 2</a></li>
            <li><a href="">Nav 3</a></li>
        </ul>
    </nav> -->
    <div class="main-panel">
        <div class="panel__box">
            <div class="img-container" v-bind:style="{ 'background-image': imgUrl}">
                <div class="img-overlay-menu">
                    <div></div>
                    <div></div>
                    <div class="menu-btm">
                        <rangeslider class="menu-slider" id="menuSlider" :initVal="currAttrVal" :min="-15" :max="15" @changedAttr="onCoeffChange"></rangeslider>
                    </div>
                </div>
            </div>
            <div class="attrs-selector">
                <ul class="list list--buttons">
                    <li v-for="attr in filteredAttr">
                        <button class="list__btn" :class="isAttrSelected(attr)" @click="changeSelectedAttr(attr)">
                            <i :class="getIcon(attr.icon)"></i>
                        </button>
                    </li>
                </ul>
            </div>
        </div>
    </div> 
    <div class="main-tabs">
        <div class="tabs__box">
            <ul class="list list--buttons">
                <li v-for="attrTab in attributeTabs">
                    <button class="tab__btn" :class="isAttrTabSelected(attrTab)" @click="changeSelectedTab(attrTab)">
                    <i class='fas' v-bind:class="attrTab.icon"></i></button>
                </li>
            </ul>
        </div>
    </div>
    <!-- <aside class="side">Sidebar</aside> -->
    <!-- <div class="ad">Advertising</div> -->
    <footer class="main-footer">The footer</footer>
</div>
    
    <!-- <socket-comp ref="socketComp" @gotImage="displayImage"></socket-comp>
  <div class="player__container">
    <div class="player__body">

        <div class="body__tabs">
            
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
    <div class="main-head"><logoHeading></logoHeading></div> -->

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
            showGallery() {
                this.$router.push('gallery');
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
            },
            saveLatent() {
                this.$refs.socketComp.sendEditAction("saveLatent", {});
            },
        }
    }
</script>

<style lang="scss" scoped>
$white: #ffffff;
$color-red: #d30320;
$dark: rgba(52, 55, 61, 0.6);
%neuBox {
    background-color: #f5f6f7;
    border-radius: 3px;
    box-shadow: -4px -2px 4px 0px  $white, 4px 2px 6px 0px $dark;
    margin: 0 auto;
}
%neuBtn {
    color: inherit;
    position: relative;
    background: inherit;
    outline: none;
    border: none;
    border-radius: 5px;
    box-shadow: -4px -2px 4px 0px  $white, 4px 2px 6px 0px $dark;
}
.wrapper {
    display: grid;
    width: 100vw;
    height: 100vh;
    @media only screen and (max-width: 640px) {
        grid-gap: 5px;
    }
    grid-gap: 2px;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: 0.2fr 2.0fr 1.2fr;
    @media only screen and (max-width: 640px) {
        grid-template-rows: 0.2fr 4fr 1fr;
    }
}
.main-head {
    grid-column: 1/6;
    grid-row: 1;
    justify-self: center;
}
.main-panel {
  grid-column: 1 / 6;
  grid-row: 2;
  .panel__box {
        @extend %neuBox;
        max-width: 600px;
        height: 60vh;
        @media only screen and (max-width: 640px) {
            margin: 0 auto;
            height: 82vh;
        }
        .img-container {
            margin: 0 auto;
            margin-bottom: 5px;
            width: 100%;
            height: 50vh;
            background-repeat: no-repeat;
            background-size: auto;
            background-position: center;
            z-index: 1;
            @media only screen and (max-width: 640px) {
                width: 95%;
                height: 70vh;
            }
            .img-overlay-menu {
                padding-top: 10px;
                padding-bottom: 10px;
                display: grid;
                height: 50vh;
                @media only screen and (max-width: 640px) {
                    height: 70vh;
                }
                grid-template-rows: 1fr 5fr 0.3fr;
                grid-template-columns: auto;
                .menu-btm {
                    align-self: end;
                    .menu-slider {
                        width: 100%;
                    }
                }
            }
        }
        .attrs-selector {
            height: 10vh;
            margin: 0 auto;
            .list {
                margin-top: 20px;
                padding: 0;
                list-style-type: none;
                &.list--buttons {
                    display: flex;
                    align-items: center;
                    justify-content: space-around;
                    flex-grow: 1;
                    flex-basis: 20%;
                    .list__btn {
                        @extend %neuBtn;
                        width: 50px;
                        height: 50px;
                        @media only screen and (max-width: 640px) {
                            width: 40px;
                            height: 40px;
                        }
                        &:hover {
                            color: darken(rgba($color-red, .95), 8%);
                            opacity: 1;
                        }
                        &.isSelected {
                            color: darken(rgba($color-red, .95), 8%);
                            box-shadow: 0px 0px 1px 1px $white inset, 2px 2px 2px 0px $dark inset;
                        }
                    }
                }
            }
        }
  }
}
.main-tabs {
    grid-column: 1 / 6;
    grid-row: 3;
    .tabs__box {
        @extend %neuBox;
        height: 50px;
        padding-top: 10px;
        @media only screen and (max-width: 640px) {
            padding-top: 0px;
            height: 30px;
        }
        max-width: 600px;
        .list {
            margin-top: 0;
            padding: 0;
            list-style-type: none;
            &.list--buttons {
                display: flex;
                align-items: center;
                justify-content: space-around;
                flex-grow: 1;
                flex-basis: 20%;
                .tab__btn {
                    @extend %neuBtn;
                    width: 50px;
                    height: 30px;
                    &:hover {
                        color: darken(rgba($color-red, .95), 8%);
                        opacity: 1;
                    }
                    &.isSelected {
                        color: darken(rgba($color-red, .95), 8%);
                        box-shadow: 0px 0px 1px 1px $white inset, 2px 2px 2px 0px $dark inset;
                    }
                }
            }
        }
    }
}
.main-footer {
    grid-column: 1 / 6;
    grid-row: 4;
}
</style>