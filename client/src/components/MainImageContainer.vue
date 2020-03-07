<template>
<div class="parent">
    <div class="img-container" v-bind:style="{ 'background-image': imgUrl}">
        <div class="img-overlay-menu">
            <div class="menu-top">
                <button type="button" @click="saveLatent"><i class='fas fa-save icon'></i></button>
                <search-expand @onEnter="onSearchEnter"></search-expand>
                <button type="button" @click="showGallery"><i class='fas fa-archive icon'></i></button>
            </div>
            <div class="menu-side left" :class="{compact:!showStyleMix}">
                <div class="tabs">
                    <input type="button" value="Style Mixing" class="tab_btn" @click="showStyleMix=!showStyleMix"/>
                    <!-- <input type="button" value="Rotated text" class="tab_btn" /> -->
                </div>
                <div v-if="showStyleMix" class="expanded-menu">
                    <stylemix-menu></stylemix-menu>
                </div>
            </div>
            <div class="menu-btm">
                <button type="button" @click="randomize"><i class='fas fa-random icon'></i></button>
                <rangeslider class="menu-slider" id="menuSlider" :initVal="currAttrVal" :min="-15" :max="15" @changedAttr="onCoeffChange"></rangeslider>
                <button type="button" @click="randomize"><i class='fas fa-random icon'></i></button>
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
</template>

<script>
import searchExpand from '@/components/FancySearch.vue';
import rangeslider from '@/components/RangeSlider.vue';
import scrollGallery from '@/components/VerticalScrollImg.vue';
import checkboxPicker from '@/components/CheckboxPicker.vue';
import stylemixMenu from '@/views/StyleMixMenu.vue';
import { mapState, mapActions, mapMutations } from 'vuex'
export default {
    name:"imgContainer",
    components: {
        rangeslider: rangeslider,
        searchExpand: searchExpand,
        checkboxPicker: checkboxPicker,
        scrollGallery: scrollGallery,
        stylemixMenu: stylemixMenu
    },
    computed: mapState({
        mainFaceImg: state => state.socketStore.mainFaceImg
    }),
    watch: {
        mainFaceImg:  {
            handler: function(n, o) {
                this.loadServerImg(n);
            },
            deep: true,
            immediate: true
        }
    },
    data() {
        return {
            imgUrl: "",
            selectedAttrTab: 'basic',
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
            filteredAttr: [],
            currSelectedAttr: null,
            currAttrVal: 0,
            showStyleMix: false
        }
    },
    mounted() {
        this.loadDefaultImg();
        this.calculateFilteredAttr(this.selectedAttrTab);
    },
    methods: {
        ... mapActions('socketStore', [
            'sendEditAction'
        ]),
        loadDefaultImg() {
            var img = 'url("./resImg.jpg")';
            this.imgUrl = img;
        },
        loadServerImg(imgUrl) {
            this.imgUrl = imgUrl;
        },
        calculateFilteredAttr(selectedTab) {
            this.selectedAttrTab = selectedTab;
            this.filteredAttr = this.attributes.filter(a => {
                return a.tabTag === this.selectedAttrTab;
            });
            this.changeSelectedAttr(this.filteredAttr[0]);
        },
        getIcon(iconClass) {
            return iconClass + " fa-lg fa-fw";
        },
        isAttrSelected(attr) {
            if(attr.name === this.currSelectedAttr.name) {
                return "isSelected";
            }
            return ""
        },
        changeSelectedAttr(attr) {
            this.currSelectedAttr = attr;
            this.currAttrVal = Number(this.currSelectedAttr.coeff);
        },
        //Image overlay events
        showGallery() {
            this.$router.push('gallery');
        },
        onSearchEnter(val) {
            // console.log(val);
            this.searchTxt = val;
            this.searchImg();
        },
        //Image Edit Actions to Server
        onCoeffChange(coeff) {
            // console.log("coeff ", coeff);
            this.currSelectedAttr.coeff = coeff;
            this.currAttrVal = Number(coeff);
            let params = this.currSelectedAttr;
            let msg = {};
            msg.action = "changeCoeff";
            msg.params = params;
            this.sendEditAction(msg);
        },
        saveLatent() {
            let msg = {};
            msg.action = "saveLatent";
            msg.params = {};
            this.sendEditAction(msg);
        },
        randomize() {
            let msg = {};
            msg.action = "randomize";
            msg.params = {};
            this.sendEditAction(msg);
        },
        searchImg() {
            let msg = {};
            msg.action = "sendSearchedImages";
            msg.params = {"text": this.searchTxt};
            this.sendEditAction(msg);
        },
        onStyleMix() {

        }
    }
}
</script>

<style lang="scss" scoped>
$white: #ffffff;
$color-red: #d30320;
$dark: rgba(52, 55, 61, 0.6);
%neuBtn {
    color: inherit;
    position: relative;
    background: inherit;
    outline: none;
    border: none;
    border-radius: 5px;
    box-shadow: -4px -2px 4px 0px  $white, 4px 2px 6px 0px $dark;
}
%overlayBtn {
    background: transparent;
    outline: none;
    border: none;
    cursor: pointer;
    &:hover {
        color: darken(rgba($color-red, .95), 8%);
        opacity: 1;
    }
}

.img-container {
    margin: 0 auto;
    margin-bottom: 0px;
    width: 100%;
    height: 65vh;
    background-repeat: no-repeat;
    background-size: auto;
    background-position: center;
    z-index: 1;
    @media only screen and (max-width: 640px) {
        width: 95%;
        height: 70vh;
    }
    .img-overlay-menu {
        padding-top: 20px;
        padding-bottom: 30px;
        display: grid;
        height: 65vh;
        @media only screen and (max-width: 640px) {
            padding-top: 10px;
            padding-bottom: 10px;
            height: 70vh;
        }
        grid-template-rows: 1fr 5fr 0.3fr;
        grid-template-columns: auto;
        .menu-btm {
            align-self: end;
            display: flex;
            align-items: center;
            justify-content: space-between;
            .menu-slider {
                width: 100%;
            }
            button {
                @extend %overlayBtn;
            }
        }
        .menu-top {
            align-self: top;
            background: rgba(#f5f6f7, 0.3);
            height: 2.1rem;
            width: 100%;
            border-radius: 5rem;
            box-shadow: 1px 5px 5px rgba(black, 0.3);
            padding-bottom: 10px;
            @media only screen and (max-width: 640px) {
                padding-bottom: 0px;
            }
            padding-left: 10px;
            padding-right: 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;

            button {
                @extend %overlayBtn;
            }
        }
        .menu-side {
            @media only screen and (min-width: 640px) {
                display: none;
            }
            display: grid;
            grid-template-columns: 30px 0.9fr;
            grid-gap: 5px;
            grid-auto-rows: auto;
            grid-template-areas: 
                "a b b";
            .tabs {
                grid-area: a;
                background: rgba(#f5f6f7, 0.3);
                height: 50vh;
                width: 100%;
                display: inline-flex;
                flex-direction: column;
                align-items: center;
	            align-self: center;
                justify-content: space-around;
                .tab_btn {
                    background: rgba(#1e1e1f, 0.7);
                    outline: none;
                    border: none;
                    border-radius: 5rem;
                    cursor: pointer;
                    -webkit-transform:rotate(90deg);
                    height: 30px;
                    width: 120px;
                    font-size: 15px;
                    text-transform: uppercase;
                    font-weight: 700;
                    color: #e9c9a9;
                    font-family: 'Dancing Script'
                }
            }
            .expanded-menu {
                grid-area: b;
                background: rgba(#f5f6f7, 0.3);
                height: 50vh;
                width: 40vw;
                 border-radius: 2rem;
                box-shadow: 1px 5px 5px rgba(black, 0.3);
                padding-left: 10px;
                padding-right: 10px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
        }
    }
}
.attrs-selector {
    margin: 0 auto;
    .list {
        @media only screen and (max-width: 640px) {
            margin-top: 20px;
        }
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
.vert{
  vertical-align:top;
	transform:rotate(7deg);
  -ms-transform:rotate(90deg); /* IE 9 */
  -moz-transform:rotate(90deg); /* Firefox */
  -webkit-transform:rotate(90deg); /* Safari and Chrome */
  -o-transform:rotate(90deg); /* Opera */
}
</style>