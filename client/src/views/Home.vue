<template>
<div>
    <div class="title">
        <logo-heading></logo-heading>
    </div>
    <div class="front">
        <div class="sidemenu left">

        </div>
        <div class="container">
            <header>
                <nav>
                    <!-- <button type="button" class="menuBtn" @click="getAttributes"><i class='fas fa-link icon'></i></button> -->
                    <button type="button" class="menuBtn" @click="saveLatent"><i class='fas fa-save icon'></i></button>
                    <search-expand @onEnter="searchEnter"></search-expand>
                    <button type="button"  class="menuBtn" @click="randomize"><i class='fas fa-random icon'></i></button>
                </nav>
            </header>
            <main>
                <div class="imgParent" id="faceImg" v-bind:style="{ 'background-image': faceImageBG}"></div>
            </main>
        </div>
        <div class="sidemenu right">
            <div class="wrapper">
                <div class="item1">
                    <nav>
                        <button @click="reset" class='attrTabBtn'><i class='fas fa-sync icon'></i></button>
                        <button v-for="attrTab in attributeTabs" type="button" v-bind:class="getTabClass(attrTab)"  @click="selectTab(attrTab)"><i class='fas' v-bind:class="attrTab.icon"></i></button>
                    </nav>
                </div>
                <div class="item2">
                    <nav>
                        <div class="attrTabTitle">
                            <span>{{selectedAttrTab}}</span>
                        </div>
                        <div v-for="attr in filteredAttr">
                            <div class="d-flex flex-row">
                                <div class="p-3">
                                    <!-- <span class="mr-3">{{attr.name}}</span> -->
                                    <i v-bind:class="getIcon(attr.icon)"></i>
                                </div>
                                <div class="p-1 align-middle">
                                    <button type="button" @click="decCoeff(attr)"><i class='fas fa-minus'></i></button>
                                </div>
                                <div class="p-1">
                                    <ripple-counter :txt="attr.coeff"></ripple-counter>
                                </div>
                                <div class="p-1">
                                    <button type="button" @click="incCoeff(attr)"><i class='fas fa-plus'></i></button>
                                </div>
                                <!-- <div class="p-1">
                                    <input type="checkbox" v-model="attr.freeze">
                                </div> -->
                            </div>
                        </div>
                        <!-- <button  type="button" class="attrTab"  @click="selectTab">{{attr.name}}</button> -->
                    </nav>
                </div>
            </div>
        </div>
    </div>
    <div class="grid">
        <fractalGrid :galleryImgs="galleryImgs"></fractalGrid>
    </div>
</div>
</template>

<script>
import rippleBtn from '@/components/RippleButton.vue';
import rippleCounter from '@/components/RippleCounter.vue';
import radialBtn from '@/components/RadialButton.vue';
import searchExpand from '@/components/FancySearch.vue';
import fractalGrid from '@/components/FractalGrid.vue';
import logoHeading from '@/components/LogoHeading.vue';

    export default {
        name: "neuMenu",
        components: {
            logoHeading: logoHeading,
            rippleBtn: rippleBtn,
            rippleCounter: rippleCounter,
            radialBtn: radialBtn,
            searchExpand: searchExpand,
            fractalGrid: fractalGrid
        },
        computed: {
        },
        data() {
            return {
                //socket
                connected: false,
                socket: null,
                logs: [],
                training: true,
                myText: "hello",
                //face editing
                attributeTabs: [
                    {name: 'basic', icon: 'fa-dna'},
                    {name: 'emotion', icon: 'fa-grin-beam'},
                    {name: 'structure', icon: 'fa-hammer'}
                ],
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
                src_face: null,
                faceImageBG: "",
                fix_layer_ranges: [0,8],
                ripples: [],
                searchTxt:"hair is brown",
                faceAttributes: {
                    smile: 0.0,
                    gender: "female",
                    glasses: "NoGlasses",
                    age: 21,
                    facialHair: {
                        moustache: 0,
                        beard: 0,
                        sideburns: 0
                    },
                    makeup: {
                        eyeMakeup: false,
                        lipMakeup: false
                    },
                    hair: {
                        bald: 0,
                        hairColor: "brown"
                    }
                },
                galleryImgs: []
            }
        },
        mounted(){
            this.connectSocket();
            this.init();
        },
        methods: {
            getIcon(iconClass) {
                return iconClass + " fa-lg fa-fw";
            },
            getTabClass(attrTab) {
                if(attrTab.name === this.selectedAttrTab) {
                    return "attrTabSelected";
                }
                return "attrTab";
            },
            selectTab(attrTab) {
                this.selectedAttrTab = attrTab.name;
                this.calculateFilteredAttr();
            },
            reset() {
                this.sendEditAction("clear", {});
                this.attributes.forEach(a => {
                    a.coeff = 0.0;
                    a.freeze = true;
                });
            },
            init() {
                //Calculate filterAttributes
                this.calculateFilteredAttr();
            },
            calculateFilteredAttr() {
                this.filteredAttr = this.attributes.filter(a => {
                    return a.tabTag === this.selectedAttrTab;
                });
            },
            connectSocket() {
                this.socket = io.connect('http://127.0.0.1:5000');
                if(this.socket.disconnected) {
                    this.loadDefaultImg();
                }
                this.socket.on('connect',()=>{
                    console.log("connected");
                    this.onConnected();
                });
                this.socket.on('logs',(logs)=>{
                    console.log(logs);
                    this.handleLogs(logs);
                });
                this.socket.on('General',(content)=>{
                    console.log('General ', content.action);
                    this.handleGeneralMsg(content);
                });
                this.socket.on('error', (err) => {
                    console.log("Error!", err);
                });
            },
            loadDefaultImg() {
                // var base64Data = a.images[0].data;
                console.log("loadDefaultImg");
                var img = 'url("./resImg.jpg")';
                console.log(img);
                this.faceImageBG = img;
            },
            onConnected() {
                this.socket.emit('init', this.training);
                this.connected = true;
                this.reset();
            },
            handleLogs(msg) {
                if(msg.logid) {
                    if(msg.type == "replace") {
                        let found = this.logs.find(l => {
                            return l.logid == msg.logid;
                        });
                        if(found) {
                            found.log = msg.log;
                        } else {
                            this.logs.push(msg);
                        }
                    }
                } else {
                    this.logs.push(msg);
                }
            },
            handleGeneralMsg(content) {
                if(content.action) {
                    if(content.action == "sendImg") {
                        this.handleReceivedImg(content);
                    } else if(content.action == "sendAttr") {
                        this.handleReceivedAttr(content);
                    } else if(content.action == "sendGalleryReset") {
                        this.galleryImgs = [];
                    }
                }
            },
            // GAN TOol
            initApp() {
                let params = {"test": "hello"};
                // this.socket.emit('initApp', msg);
                this.sendEditAction("initApp", params);
            },
            handleReceivedImg(content) {
                if(content.tag.includes("gallery")) {
                    // console.log(content.tag);
                    let galleryIdx = content.tag.split("gallery")[1]
                    console.log("galleryIdx ", galleryIdx);
                    let galleryImg = {};
                    galleryImg.galleryIdx = galleryIdx;
                    content.fig.axes.forEach(a => {
                        var base64Data = a.images[0].data;
                        galleryImg.png = base64Data;
                    });
                    this.galleryImgs.push(galleryImg);
                } else {
                    content.fig.axes.forEach(a => {
                        // console.log(a.images[0].data);
                        var base64Data = a.images[0].data;
                        var img = "url('data:image/png;base64, "+base64Data + "')";
                        // document.body.style.backgroundImage = img; 
                        this.faceImageBG = img;
                        // this.src_face = {data: a.images[0].data, fn: content.filename};
                        // var tmp_path = URL.createObjectURL('path/to/image.png');
                    });
                }
            },
            handleReceivedAttr(content) {
                console.log(content);
                let attrReceived = content.attr[0].faceAttributes;
                this.faceAttributes.smile = attrReceived.smile;
                this.faceAttributes.gender = attrReceived.gender;
                this.faceAttributes.glasses = attrReceived.glasses;
                this.faceAttributes.age = attrReceived.age;
                this.faceAttributes.facialHair = attrReceived.facialHair;
                this.faceAttributes.makeup = attrReceived.makeup;
                this.faceAttributes.hair.bald = attrReceived.hair.bald;
                this.faceAttributes.hair.hairColor = attrReceived.hair.hairColor[0].color;
            },
            testFunc() {
                console.log("testFunc");
            },
            changeAttr(idx) {
                let attr = null;
                if(idx == 0) { //smile
                    attr = this.attributes[0];
                    attr.coeff += 0.25;
                } else if(idx == 1) { //frown
                    attr = this.attributes[0];
                    attr.coeff -= 0.25;
                } else if(idx == 2) { //gender
                    attr = this.attributes[1];
                    attr.coeff += 0.25;
                } else if(idx == 3) { //gender
                    attr = this.attributes[2];
                    attr.coeff -= 0.25;
                }
                if(attr != null) {
                    this.changeCoeff(attr);
                }
                // console.log(attr.name, attr.coeff);
            },
            randomize() {
                let params = {};
                this.sendEditAction("randomize", params);
            },
            decCoeff(attr) {
                attr.coeff -= 0.5;
                this.changeCoeff(attr);
            },
            incCoeff(attr) {
                attr.coeff += 0.5;
                this.changeCoeff(attr);
            },
            changeCoeff(attr) {
                let params = attr;//{"attrName":attr.name, "coeff": attr.coeff, "clipTop": attr.clipTop, "clipBottom": attr.clipBottom};
                this.sendEditAction("changeCoeff_clipped", params);
            },
            getAttributes() {
                this.sendEditAction("getAttributes", {});
            },
            saveLatent() {
                this.sendEditAction("saveLatent", {});
            },
            searchEnter(val) {
                // console.log(val);
                this.searchTxt = val;
                this.searchImg()
            },
            searchImg() {
                this.sendEditAction("sendSearchedImages", {"text": this.searchTxt});
            },
            sendEditAction(actionName, params) {
                let msg = {};
                msg.action = actionName;
                msg.params = params;
                if(this.socket) {
                    this.socket.emit('editAction', msg);
                }
            },
        }
    }
</script>

<style scoped lang="scss">
.title {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
}
.front {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
}
$radius: 3px;
$gray-100: hsla(210, 38%, 95%, 1);
$muted: hsla(214, 25%, 65%, 1);
$white: #ffffff;
$black: #4a5568;
$shocking-pink: #ff1ead;
$dark: #DFE4EA;
$shadow-tl: -4px -2px 4px 0px;
$shadow-tl2: -4px -2px 0px 0px;
$shadow-br: 4px 2px 6px 0px;
$shadow-br2: 14px 2px 6px 0px;

#faceImg {
    margin: 0 auto;
    width: 512px;
    height: 512px;
    background-repeat: no-repeat;
    background-size: auto;
}
.imgParent {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}


$shadow: $shadow-tl $white, $shadow-br $dark;
$shadow-flip: $shadow-tl $dark inset, $shadow-br $white inset;
$shadow2: $shadow-tl2 $white, $shadow-br2 $dark;

%button {
    color: inherit;
    position: relative;
    background: inherit;
    outline: none;
    border: none;
    box-shadow: $shadow;
}

%button2 {
    color: inherit;
    position: relative;
    background: inherit;
    outline: none;
    border: none;
    box-shadow: $shadow2;
}
%button2-focus {
    color: inherit;
    position: relative;
    background: inherit;
    outline: none;
    border: none;
    box-shadow: 2px 2px 2px 0px $dark inset, -2px -2px 2px 0px $white inset;
}

%button-focus {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    border-radius: $radius;
    box-shadow: 2px 2px 2px 0px $dark inset, -2px -2px 2px 0px $white inset;
}

.container {
    background-color: #f5f6f7;
    height: 600px;
    width: 600px;
    padding: 1rem 1.5rem;
    border-radius: $radius;
    box-shadow: $shadow;
    text-transform: uppercase;
    // margin: auto;
    margin-right: 0;
    margin-left: 0;

    nav {
        display: flex;
        justify-content: space-between;
    }
}
.sidemenu {
    background-color: #f5f6f7;
    height: 400px;
    width: 240px;
    border-radius: $radius;
    box-shadow: $shadow;
    padding: 10px 20px 20px 0px;
    // margin: auto;
    .left {
        margin-right: 0;
    }
    .right {
        margin-left: 0;
    }

    .wrapper {
        display: grid;
        grid-template-columns: 0.5fr 2.5fr;
        grid-gap: 5px;
        grid-auto-rows: auto;
        grid-template-areas: 
            "a b b";

            .item1 {
                grid-area: a;
                nav {
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    height: 380px;

                    .attrTab {
                        @extend %button2;
                        background: #f5f6f7;
                        width: 30px;
                        height: 70px;
                    }
                    .attrTabSelected {
                        @extend %button2-focus;
                        background: #f5f6f7;
                        width: 30px;
                        height: 70px;
                    }
                    .attrTabBtn {
                        @extend %button2;
                        background: #f5f6f7;
                        width: 30px;
                        height: 40px;
                    }
                }
            }
            .item2 {
                grid-area: b;
                justify-self: start;
                nav {
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    height: 380px;
                }
                button {
                    @extend %button;
                    width: 30px;
                    z-index: 2;
                }
                .attrTabTitle {
                    display: flex;
                    justify-content: center;
                    font-family: "Paytone One";
                    color: #202020;
                    text-transform: uppercase;
                    font-weight: 600;
                }
            }
    }

}
.grid {
    background-color: #f5f6f7;
    height: 100%;
    width: 100%;
    padding: 1rem 1.5rem;
    border-radius: $radius;
    box-shadow: $shadow;
}

.menuBtn {
    @extend %button;
    width: 50px;

    &:focus,
    &:active {
        &::after {
            @extend %button-focus;
        }
    }
}
.icon {
    color: black;
}
</style>