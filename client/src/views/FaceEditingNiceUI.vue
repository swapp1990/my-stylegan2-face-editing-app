<template>
    <div class="test">
        <!-- <button :class="getConnectClass()" @click="connectSocket()"><i class="icon-magnet"></i></button> -->
        <div v-if="connected">
            <div class="p-2">
                <div>Face Editing</div>
                <div class="row">
                    <div class="col-sm-6" id="faceImg" v-bind:style="{ 'background-image': faceImageBG}">
                        <a href='#' class='cta'>
                            <i class='fas fa-check icon'></i>
                        </a>
                        <!-- <button @click="clear()">Clear</button>
                        <button @click="randomize()">Random</button> -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "FaceEditNiceUI",
    components: {
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
            fix_layer_ranges: [0,8]
        }
    },
    mounted(){
        this.connectSocket();
    },
    methods: {
        reset() {

        },
        getConnectClass() {
            let classes = [];
            if(this.connected) {
                classes.push("btn-primary");
            } else {
                classes.push("btn-danger");
            }
            return classes;
        },
        connectSocket() {
            this.socket = io.connect('http://127.0.0.1:5000');
            this.socket.on('connect',()=>{
                console.log("connected");
                this.onConnected();
            });
            this.socket.on('disconnect',()=>{
                console.log('disconnect');
                this.onDisconnected();
            });
            this.socket.on('connect_error', (error) => {
                console.log("Error");
                this.onDisconnected();
            });
            this.socket.on('error', (err) => {
                console.log("Error!", err);
            });
            this.socket.on('logs',(logs)=>{
                console.log(logs);
                this.handleLogs(logs);
            });
            this.socket.on('General',(content)=>{
                console.log('General ', content.action);
                this.handleGeneralMsg(content);
            });
        },
        onConnected() {
            this.socket.emit('init', this.training);
            this.connected = true;
            this.reset();
        },
        onDisconnected() {
            this.socket.close();
            this.connected = false;
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
        sendEditAction(actionName, params) {
            let msg = {};
            msg.action = actionName;
            msg.params = params;
            this.socket.emit('editAction', msg);
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
        clear() {
            this.attributes.forEach(attr => {
                attr.coeff = 0;
            });
            let params = {};
            this.sendEditAction("clear", params);
        },
        randomize() {
            let params = {};
            this.sendEditAction("randomize", params);
        },
        changeCoeff(attr) {
            let params = {"attrName":attr.name, "coeff": attr.coeff};
            this.sendEditAction("changeCoeff", params);
        },
        changeLayerMixRange() {
            if (this.fix_layer_ranges[0] > this.fix_layer_ranges[1]) {
                var tmp = this.fix_layer_ranges[0];
                this.fix_layer_ranges[1] = this.fix_layer_ranges[0];
                this.fix_layer_ranges[0] = tmp;
            }
            let params = {"fix_layer_ranges":this.fix_layer_ranges};
            this.sendEditAction("changeFixedLayers", params);
        }
    }
}
</script>
<style scoped lang="scss">
    $mainC: #f1f3f6;
    $secC: #9dabc0;
    %center {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .cta {
        @extend %center; 
        width: 66px;
        height: 66px;
        background: $mainC;
        border-radius: 20px;
        box-shadow: 
            inset 0 0 15px rgba(55, 84, 170,0),
            inset 0 0 20px rgba(255, 255, 255,0),
            7px 7px 15px rgba(55, 84, 170,.15),
            -7px -7px 20px rgba(255, 255, 255,1),
            inset 0px 0px 4px rgba(255, 255, 255,.2);
        .icon {
            @extend %center; 
            color: $secC;
            height: 30px;
            width: 30px;
        }
        &:hover {
            box-shadow: 
            inset 7px 7px 15px rgba(55, 84, 170,.15),
            inset -7px -7px 20px rgba(255, 255, 255,1),
            0px 0px 4px rgba(255, 255, 255,.2);
        }
        transition: box-shadow 399ms ease-in-out;
    }
    #faceImg {
        margin: 0 auto;
        width: 512px;
        height: 512px;
        background-repeat: no-repeat;
        background-size: auto;
    }
    .selectedImg {
        border: 3px solid brown;
        border-radius: 4px;
    }
    .range-slider {
        width: 300px;
        text-align: center;
        position: relative;
    }
</style>