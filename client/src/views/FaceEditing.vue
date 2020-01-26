<template>
    <div>
        <button :class="getConnectClass()" @click="connectSocket()"><i class="icon-magnet"></i></button>
        <div v-if="connected">
            <div class="p-2">
                <hr>
                <div>Init</div>
                <button @click="initApp()"><i class="icon-bolt"></i></button>
                <div class="p-1">
                    <div v-for="l in logs">{{l.log}}</div>
                </div>
                <hr>
            </div>
            <div class="p-2">
                <div>Face Editing</div>
                <div class="row">
                    <div class="col-sm-6">
                        <img v-if="src_face != null" v-bind:src="'data:image/jpeg;base64,'+src_face.data"/>
                    </div>
                    <div class="col-sm-6">
                        <div class="row">
                            <div class="col-sm-4">
                                <button @click="clear()">Clear</button>
                                <button @click="randomize()">Random</button>
                            </div>
                            <div class="col-sm-8">
                                <div class="p-2">
                                    <div class="range-slider">
                                        <span>Fix DLatent Layers from {{fix_layer_ranges[0]}} to {{fix_layer_ranges[1]}}</span><br>
                                        <input @change="changeLayerMixRange" v-model.number="fix_layer_ranges[0]" min="0" max="18" step="1" type="range" />
                                        <input @change="changeLayerMixRange" v-model.number="fix_layer_ranges[1]" min="0" max="18" step="1" type="range" />
                                    </div>
                                </div>
                            </div>
                        </div>
                        <hr>
                        <div v-for="attr in attributes" class="p-2">
                            <span class="mr-3">{{attr.name}}</span>
                            <input type="range" id="customRange1" min="-12" max="12" step="0.5" v-on:change="changeCoeff(attr)" v-model="attr.coeff">
                            <span class="ml-3">Coeff: {{attr.coeff}}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "FaceEditView",
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
                this.src_face = {data: a.images[0].data, fn: content.filename};
                // this.raw_images.push({data: a.images[0].data, fn: content.filename});
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
<style scoped>
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