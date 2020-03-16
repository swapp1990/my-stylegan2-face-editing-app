<template>
<div class="wrapper">
    <b-modal id="login-modal" hide-footer title="Login">
        <div>Please enter user name or create a new one </div>
        username: <input type="text" v-model="username">
        <b-button class="mt-3" variant="outline-danger" block @click="hideModal">Ok</b-button>
    </b-modal>
    <div class="wrapper-grid">
        <div class="header">
            <logoHeading></logoHeading>
        </div>
        <div class="side-menu-l">
            <div class="panel-side left">
                <stylemix-menu></stylemix-menu>
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
                        <button class="tab__btn" :class="isAttrTabSelected(attrTab)" @click="changeSelectedTab(attrTab)" v-b-tooltip.hover :title="attrTab.hoverText">
                        <i class='fas' v-bind:class="attrTab.icon"></i></button>
                    </li>
                </ul>
            </div>
        </div>
        <div class="footer">
            <fractalGrid :galleryImgs="galleryImgs"></fractalGrid>
        </div>
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
import stylemixMenu from '@/views/StyleMixMenu.vue';
import { mapState, mapActions, mapMutations } from 'vuex'

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
            stylemixMenu: stylemixMenu
        },
        computed: mapState({
            galleryImgs_store: state => state.socketStore.galleryImgs,
            isConnected: state => state.socketStore.isConnected
        }),
        watch: {
            galleryImgs_store:  {
                handler: function(n, o) {
                    this.loadGallery(n);
                },
                deep: true,
                immediate: true
            }
        },
        data() {
            return {
                username: "",
                //face editing
                attributeTabs: [
                    {name: 'basic', icon: 'fa-dna', hoverText: 'basic'},
                    {name: 'emotion', icon: 'fa-grin-beam', hoverText: 'emotions'},
                    {name: 'structure', icon: 'fa-hammer', hoverText: 'structure'}
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
            }
        },
        mounted() {
            // if(!this.isConnected) {
            //     this.connectServer();
            // }
            if(!this.isConnected) {
                this.$bvModal.show('login-modal')
            }
        },
        methods: {
           ... mapActions('socketStore', [
                'connectServer',
                'sendEditAction'
            ]),
            hideModal() {
                console.log(this.username);
                if(this.username !== "" && this.username.length < 10) {
                    this.$bvModal.hide('login-modal');
                    this.connectServer(this.username);
                }
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
            loadGallery(imgArr) {
                if(imgArr == null) return;
                this.galleryImgs = imgArr;
            },
            showGallery() {
                this.$router.push('gallery');
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
                this.$refs.imgCont.calculateFilteredAttr(this.selectedAttrTab);
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
    @media only screen and (max-width: 1000px) {
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
        // display: grid;
        // grid-template-columns: 0.3fr 0.7fr;
        // grid-gap: 5px;
        // grid-auto-rows: auto;
        // grid-template-areas: 
        //     "a b b";
    }
    &.right {
        margin-left: 0;
        display: none;
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
    @media only screen and (max-width: 640px) {
        display: none;
    }
    @extend %commonLayoutOptsMobile;
    // background-color: #fff;
    grid-area: footer;
    border-radius: 5px;
}
</style>