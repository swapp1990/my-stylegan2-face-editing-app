<template>
<div class="wrapper">
    <div class="wrapper-grid">
        <div class="header">
            <logoHeading></logoHeading>
        </div>
        <div class="side-menu-l">
            <div class="panel-side left">
                <div class="item1 thinScroll">
                    <checkbox-picker :initMax="5" v-on:checked="onMixLayerPicked"></checkbox-picker>
                </div>
                <div class="item2 thinScroll">
                    <scroll-gallery :mixImgs="galleryMixImgs" @onMiximgClick="onMiximgClick"></scroll-gallery>
                </div>
            </div>
        </div>
        <div class="main-body">
            <div class="panel__box">
                <img-container ref="imgCont"></img-container>
            </div>
        </div>
        <div class="side-menu-r">
            <div class="panel-side right">
            </div>
        </div>
        <div class="btm-menu">
            <div class="panel-btm">
                <ul class="list list--buttons">
                    <li v-for="attrTab in attributeTabs">
                        <button class="tab__btn" :class="isAttrTabSelected(attrTab)" @click="changeSelectedTab(attrTab)">
                        <i class='fas' v-bind:class="attrTab.icon"></i></button>
                    </li>
                </ul>
            </div>
        </div>
        <div class="footer">C</div>
    </div>
</div>
</template>

<script>
import imgContainer from '@/components/MainImageContainer.vue';
import logoHeading from '@/components/LogoHeading.vue';
import neubox from '@/components/NeuBox.vue';
import rangeslider from '@/components/RangeSlider.vue';
import socketComp from '@/components/Socket.vue';
import searchExpand from '@/components/FancySearch.vue';
import fractalGrid from '@/components/FractalGrid.vue';
import scrollGallery from '@/components/VerticalScrollImg.vue';
import checkboxPicker from '@/components/CheckboxPicker.vue';
    export default {
        name: "homenew",
        components: {
            imgContainer: imgContainer,
            logoHeading: logoHeading,
            neubox: neubox,
            rangeslider: rangeslider,
            socketComp: socketComp,
            searchExpand: searchExpand,
            fractalGrid: fractalGrid,
            scrollGallery: scrollGallery,
            checkboxPicker: checkboxPicker,
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
                galleryImgs: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                galleryMixImgs: ["1", "2", "3", "4", "5"],
                layersMixMap: [],
                selectedImgIdx: 0
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
                // this.calculateFilteredAttr();
                this.$refs.imgCont.calculateFilteredAttr(this.selectedAttrTab);
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
            randomize() {
                this.$refs.socketComp.sendEditAction("randomize", {});
            },
            searchEnter(val) {
                // console.log(val);
                // this.searchTxt = val;
                this.searchImg()
            },
            searchImg() {
                // this.sendEditAction("sendSearchedImages", {"text": this.searchTxt});
            },
            onMiximgClick(imgIdx) {
                this.selectedImgIdx = imgIdx;
                // let params = {"styleImgIdx": imgIdx, "layersMixMap": this.layersMixMap};
                // this.sendEditAction("mixStyleImg", params);
            },
            onMixLayerPicked(vals) {
                this.layersMixMap = vals;
                let params = {"styleImgIdx": this.selectedImgIdx, "layersMixMap": this.layersMixMap};
                // this.sendEditAction("mixStyleImg", params);
            },
        }
    }
</script>

<style lang="scss" scoped>
html,
body {
width: 100vw;
height: 100vh;
}
$white: #ffffff;
$red: #d30320;
$dark: rgba(52, 55, 61, 0.6);
$max-body-w: 600px;
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
%overlayBtn {
    background: transparent;
    outline: none;
    border: none;
    cursor: pointer;
    &:hover {
        color: darken(rgba($red, .95), 8%);
        opacity: 1;
    }
}
%commonLayoutOptsMobile {
    padding: 5px;
    margin: 1px;
    @media only screen and (max-width: 640px) {
        padding: 5px;
        margin: 1px;
    }
}
.thinScroll::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
	border-radius: 10px;
	background-color: #F5F5F5;
}
.thinScroll::-webkit-scrollbar
{
	width: 5px;
	background-color: #F5F5F5;
}
.thinScroll::-webkit-scrollbar-thumb
{
	-webkit-box-shadow: inset 0 0 6px rgba(0,0,0,.3);
	background-color: rgba($red, .55);
}
.wrapper {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
}
.wrapper-grid {
    width: 80vw;
    height: 100vh;
    display: grid;
    grid-gap: 0px;
    grid-template-columns: 0.8fr 600px 0.8fr;
    grid-template-rows: 10% 75% 10% 5%;
    grid-template-areas:
        "header header header"
        "sml mb smr"
        "bm bm bm"
        "footer footer footer";
    @media only screen and (max-width: 640px) {
        width: 100vw;
        grid-template-columns: 1fr;
        grid-template-rows: 10% 80% 10% 5%;
        grid-template-areas:
            "header header"
            "mb mb"
            "bm bm"
            "footer footer";
    }
    
    // @media only screen and (max-width: 640px) {
    //     grid-template-columns: 1fr;
    //     grid-gap: 2px;
    //     width: 100vw;
    //     grid-template-areas:
    //         "header"
    //         "mb"
    //         "bm"
    //         "footer";
    // }
    // grid-template-columns: repeat(4, [col] 20vh ) ;
    // grid-template-rows: repeat(2, [row] auto  );
    background-color: #444;
    color: #444;
}
.header {
    @extend %commonLayoutOptsMobile;
    // background-color: #fff;
    grid-area: header;
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.side-menu-l {
    @media only screen and (max-width: 640px) {
        display: none;
    }
    @extend %commonLayoutOptsMobile;
    // background-color: #fff;
    grid-area: sml;
    border-radius: 5px;
    display: flex;
    flex-direction: row;
    align-items: center;
}
.main-body {
    @extend %commonLayoutOptsMobile;
    // background-color: #fff;
    grid-area: mb;
    border-radius: 5px;
    padding: 0;
    margin: 0;
    .panel__box {
        @extend %neuBox;
        width: 100%;
        height: 100%;
        max-width: $max-body-w;
    }
}
.side-menu-r {
    @media only screen and (max-width: 640px) {
        display: none;
    }
    @extend %commonLayoutOptsMobile;
    // background-color: #fff;
    grid-area: smr;
    border-radius: 5px;
    display: flex;
    flex-direction: row;
    align-items: center;
}
.panel-side {
    @media only screen and (max-width: 640px) {
        display: none;
    }
    @extend %neuBox;
    width: 100%;
    height: 400px;
    min-height: 0;
    max-width: 200px;
    &.left {
        @media only screen and (max-width: 640px) {
            display: none;
        }
        margin-right: 0;
        display: grid;
        grid-template-columns: 0.3fr 0.7fr;
        grid-gap: 5px;
        grid-auto-rows: auto;
        grid-template-areas: 
            "a b b";
        .item1 {
            grid-area: a;
            overflow-y: scroll;
            overflow-x: hidden;
            height: inherit;
        }
        .item2 {
            grid-area: b;
            overflow-y: scroll;
            height: inherit;
        }
    }
    &.right {
        margin-left: 0;
        @media only screen and (max-width: 640px) {
            display: none;
        }
    }
}
.btm-menu {
    @extend %commonLayoutOptsMobile;
    // background-color: #fff;
    grid-area: bm;
    border-radius: 5px;
    .panel-btm {
        height: 100%;
        display: flex;
        flex-direction: row;
        align-items: center;
        .list {
            margin-top: 0;
            margin-bottom: 0;
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
                    width: 80px;
                    height: 40px;
                    &:hover {
                        color: darken(rgba($red, .95), 8%);
                        opacity: 1;
                    }
                    &.isSelected {
                        color: darken(rgba($red, .95), 8%);
                        box-shadow: 0px 0px 1px 1px $white inset, 2px 2px 2px 0px $dark inset;
                    }
                }
            }
        }
    }
}
.panel-btm {
    @extend %neuBox;
    width: 100%;
    height: 50%;
    max-width: $max-body-w;
}
.footer {
    @extend %commonLayoutOptsMobile;
    background-color: #fff;
    grid-area: footer;
    border-radius: 5px;
}
</style>