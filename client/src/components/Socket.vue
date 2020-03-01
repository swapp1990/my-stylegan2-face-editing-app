<template>
    <div>

    </div>
</template>

<script>
    export default {
        name: "socketComp",
        mounted() {
            this.connectSocket();
        },
        data() {
            return {
                //socket
                connected: false,
                socket: null,
                logs: [],
                username: "swapp"
            }
        },
        methods: {
            connectSocket() {
                this.socket = io.connect('http://127.0.0.1:5000');
                if(this.socket.disconnected) {
                    // this.loadDefaultImg();
                }
                this.socket.on('connect',()=>{
                    console.log("connected");
                    this.onConnected();
                });
                this.socket.on('General',(content)=>{
                    console.log('General ', content.action);
                    this.handleGeneralMsg(content);
                });
            },
            onConnected() {
                console.log("On Connected");
                this.connected = true;
                // this.reset();
                this.login();
            },
            login() {
                this.socket.emit('set-session', {"user": this.username});
            },
            handleGeneralMsg(content) {
                if(content.action) {
                    if(content.action == "sendImg") {
                        this.handleReceivedImg(content);
                    }
                }
            },
            handleReceivedImg(content) {
                if(content.tag.includes("gallery")) {
                } else {
                    let imgUrl = null;
                    content.fig.axes.forEach(a => {
                        // console.log(a.images[0].data);
                        var base64Data = a.images[0].data;
                        imgUrl = "url('data:image/png;base64, "+base64Data + "')";
                    });
                    if(imgUrl != null) {
                        this.$emit("gotImage", {'imgUrl': imgUrl});
                    }
                }
            },
            sendEditAction(actionName, params) {
                let msg = {};
                msg.action = actionName;
                msg.params = params;
                if(this.socket) {
                    this.socket.emit('editAction', msg);
                }
            }
        }
    }
</script>

<style lang="scss" scoped>

</style>