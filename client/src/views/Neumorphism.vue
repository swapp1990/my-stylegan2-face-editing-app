<template>
    <div>
        <div class="container">
            <header>
                <nav>
                    <button type="button" class="menuBtn"><i class='fas fa-arrow-left icon'></i></button>
                    <search-expand text="hair is black" @onEnter="searchEnter"></search-expand>
                    <button type="button"  class="menuBtn" @click="randomize"><i class='fas fa-random icon'></i></button>
                </nav>
            </header>
            <main>
                <div class="imgParent" id="faceImg" v-bind:style="{ 'background-image': faceImageBG}">
                    <div></div>
                    <div class="attrMenu">
                        <nav>
                            <ripple-btn text="test" @click="changeAttr(0)"><i class='far fa-grin-alt icon'></i></ripple-btn>
                            <ripple-btn text="test" @click="changeAttr(1)"><i class='far fa-grin-alt icon'></i></ripple-btn>
                            <ripple-btn text="test" @click="changeAttr(2)"><i class='far fa-grin-alt icon'></i></ripple-btn>
                            <ripple-btn text="test" @click="changeAttr(3)"><i class='far fa-grin-alt icon'></i></ripple-btn>
                        </nav>
                    </div>
                </div>
                <!-- <h1 class="t1">History</h1> -->
            </main>
        </div>
        <div class="grid">
            <fractalGrid></fractalGrid>
        </div>
    </div>
    
</template>

<script>
import rippleBtn from '@/components/RippleButton.vue';
import searchExpand from '@/components/FancySearch.vue';
import fractalGrid from '@/components/FractalGrid.vue';

    export default {
        name: "neuMenu",
        components: {
            rippleBtn: rippleBtn,
            searchExpand: searchExpand,
            fractalGrid: fractalGrid
        },
        data() {
            return {
                //socket
                connected: false,
                socket: null,
                logs: [],
                training: true,
                //face editing
                attributes: [
                        {name: 'smile', coeff: 0.0}, 
                        {name: 'smilelearned', coeff: 0.0}, 
                        {name: 'gender', coeff: 0.0},
                        {name: 'age', coeff: 0.0},
                        {name: 'beauty', coeff: 0.0},
                        {name: 'glasses', coeff: 0.0},
                        {name: 'race_black', coeff: 0.0},
                        {name: 'race_yellow', coeff: 0.0},
                        {name: 'emotion_fear', coeff: 0.0},
                        {name: 'emotion_angry', coeff: 0.0},
                        {name: 'emotion_disgust', coeff: 0.0},
                        {name: 'emotion_easy', coeff: 0.0},
                        {name: 'eyes_open', coeff: 0.0},
                        {name: 'angle_horizontal', coeff: 0.0},
                        {name: 'angle_pitch', coeff: 0.0},
                        {name: 'face_shape', coeff: 0.0},
                        {name: 'height', coeff: 0.0},
                        {name: 'width', coeff: 0.0},
                    ],
                src_face: null,
                faceImageBG: "",
                fix_layer_ranges: [0,8],
                ripples: [],
                searchTxt:"hair is brown"
            }
        },
        mounted(){
            this.connectSocket();
        },
        methods: {
            reset() {

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
                content.fig.axes.forEach(a => {
                    // console.log(a.images[0].data);
                    var base64Data = a.images[0].data;
                    var img = "url('data:image/png;base64, "+base64Data + "')";
                    // document.body.style.backgroundImage = img; 
                    this.faceImageBG = img;
                    // this.src_face = {data: a.images[0].data, fn: content.filename};
                    // var tmp_path = URL.createObjectURL('path/to/image.png');
                });
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
            changeCoeff(attr) {
                let params = {"attrName":attr.name, "coeff": attr.coeff};
                this.sendEditAction("changeCoeff", params);
            },
            searchEnter(val) {
                // console.log(val);
                this.searchTxt = val;
                this.searchImg()
            },
            searchImg() {
                this.sendEditAction("sendSearchedImages", {"searchTxt": this.searchTxt});
            },
            sendEditAction(actionName, params) {
                let msg = {};
                msg.action = actionName;
                msg.params = params;
                this.socket.emit('editAction', msg);
            },
        }
    }
</script>

<style scoped lang="scss">
#faceImg {
    margin: 0 auto;
    width: 512px;
    height: 512px;
    background-repeat: no-repeat;
    background-size: auto;
}

$radius: 3px;
$gray-100: hsla(210, 38%, 95%, 1);
$muted: hsla(214, 25%, 65%, 1);
$white: #ffffff;
$black: #4a5568;
$shocking-pink: #ff1ead;
$dark: #DFE4EA;
$shadow-tl: -4px -2px 4px 0px;
$shadow-br: 4px 2px 6px 0px;
$shadow: $shadow-tl $white, $shadow-br $dark;
$shadow-flip: $shadow-tl $dark inset, $shadow-br $white inset;
    .container {
        background-color: #f5f6f7;
        height: 600px;
        width: 600px;
        padding: 1rem 1.5rem;
        border-radius: $radius;
        box-shadow: $shadow;
        cursor: pointer;
        text-transform: uppercase;
        margin-bottom: 30px;
    }
    .grid {
        background-color: #f5f6f7;
        height: 100%;
        width: 100%;
        padding: 1rem 1.5rem;
        border-radius: $radius;
        box-shadow: $shadow;
    }
    nav {
        display: flex;
        justify-content: space-between;
    }

    %button {
        color: inherit;
        position: relative;
        background: inherit;
        outline: none;
        border: none;
        box-shadow: $shadow;
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

    .menuBtn {
        @extend %button;
        padding: 0.5rem 0.75rem;

        &:focus,
        &:active {
            &::after {
                @extend %button-focus;
            }
        }
    }
    .imgParent {
        display: flex;
        flex-direction: column;
        justify-content: space-between;

        .attrMenu {
            // border: 1px solid red;
        }
    }

    .icon {
        color: black;
    }

    $sizes: 1.5rem, 1.25rem, 1rem, 0.85rem, 0.5rem;
    @for $i from 1 through length($sizes) {
        .t#{$i} {
            font-size: nth($sizes, $i);
            font-family: "Kulim Park", sans-serif;
        }
    }
</style>