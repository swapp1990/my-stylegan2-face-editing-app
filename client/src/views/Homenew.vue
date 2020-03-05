<template>
<div class="wrapper">
    <div class="wrapper-grid">
        <div class="header">
            <logoHeading></logoHeading>
        </div>
        <div class="side-menu-l">
            <div class="panel-side left">
            </div>
        </div>
        <div class="main-body">
            <div class="panel__box">
            </div>
        </div>
        <div class="side-menu-r">
            <div class="panel-side right">
            </div>
        </div>
        <div class="btm-menu">
            <div class="panel-btm">
            </div>
        </div>
        <div class="footer">C</div>
    </div>
</div>
</template>

<script>
import logoHeading from '@/components/LogoHeading.vue';
import neubox from '@/components/NeuBox.vue';
import rangeslider from '@/components/RangeSlider.vue';
import socketComp from '@/components/Socket.vue';
import searchExpand from '@/components/FancySearch.vue';
import fractalGrid from '@/components/FractalGrid.vue';
    export default {
        name: "homenew",
        components: {
            logoHeading: logoHeading,
            neubox: neubox,
            rangeslider: rangeslider,
            socketComp: socketComp,
            searchExpand: searchExpand,
            fractalGrid: fractalGrid
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
        }
    }
</script>

<style lang="scss" scoped>
$white: #ffffff;
$color-red: #d30320;
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
        color: darken(rgba($color-red, .95), 8%);
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
    grid-template-rows: 0.1fr 0.6fr 0.2fr 0.1fr;
    @media only screen and (max-width: 640px) {
        grid-template-columns: 0.1fr 2.8fr 0.1fr;
        grid-template-rows: 0.1fr 0.9fr 0.1fr 0.05fr;
    }
    grid-template-areas:
        "header header header"
        "sml mb smr"
        "bm bm bm"
        "footer footer footer";
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
    background-color: #fff;
    grid-area: header;
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.side-menu-l {
    @extend %commonLayoutOptsMobile;
    background-color: #fff;
    grid-area: sml;
    border-radius: 5px;
    display: flex;
    flex-direction: row;
    align-items: center;
}
.main-body {
    @extend %commonLayoutOptsMobile;
    background-color: #fff;
    grid-area: mb;
    border-radius: 5px;
    .panel__box {
        @extend %neuBox;
        width: 100%;
        height: 100%;
        max-width: $max-body-w;
    }
}
.side-menu-r {
    @extend %commonLayoutOptsMobile;
    background-color: #fff;
    grid-area: smr;
    border-radius: 5px;
    display: flex;
    flex-direction: row;
    align-items: center;
}
.panel-side {
    @extend %neuBox;
    width: 100%;
    height: 70%;
    max-width: 200px;
    &.left {
        margin-right: 0;
    }
    &.right {
        margin-left: 0;
    }
}
.btm-menu {
    @extend %commonLayoutOptsMobile;
    background-color: #fff;
    grid-area: bm;
    border-radius: 5px;
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