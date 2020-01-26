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
                        <div>
                            <button @click="clear()">Clear</button>
                            <button @click="randomize()">Random</button>
                        </div>
                        <div class="p-2">
                            <input type="range" id="customRange1" min="-15" max="15" step="0.5"
                    v-on:change="changeCoeff()" v-model="dirVecCoeff">
                    <span class="ml-3">Coeff: {{dirVecCoeff}}</span>
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
            src_face: null,
            dirVecCoeff: 0.0
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

        },
        randomize() {
            let params = {};
            this.sendEditAction("randomize", params);
        },
        changeCoeff() {
            let params = {"coeff": this.dirVecCoeff};
            this.sendEditAction("changeCoeff", params);
        }
    }
}
</script>
