<template>
    <div class="mixwrapper">
        <div class="topItem">
            <input type="button" value="Chats" class="header loading" />
            <!-- @click="showStyleMix=!showStyleMix"/> -->
        </div>
        <div class="item1 thinScroll">
            <ul class="chats">
                <li v-for="chats in chatsToShow">
                    {{chats.user}}: {{chats.chatTxt}}
                </li>
            </ul>
        </div>
        <div class="item3">
            <div class="bar">
                <input class="col-xs-2" type="text" v-model="chatTxt">
                <button @click="sendChat">Send</button>
            </div>
        </div>
    </div>
</template>
<script>
import { mapState, mapActions, mapMutations } from 'vuex'
export default {
    name:"chatsContainer",
    data() {
        return {
            chatTxt: "Hello",
            chatsToShow: []
        }
    },
    computed: mapState({
        isConnected: state => state.socketStore.isConnected,
        chatsArr: state => state.socketStore.chatsArr,
        cleared: state => state.socketStore.cleared,
    }),
    watch: {
        chatsArr:  {
            handler: function(n, o) {
                this.chatsToShow = n;
            },
            deep: true,
            immediate: true
        },
    },
    methods: {
        ... mapActions('socketStore', [
            'sendChatToServer'
        ]),
        sendChat() {
            this.sendChatToServer(this.chatTxt);
            this.chatTxt = ""
        }
    }
}
</script>
<style lang="scss" scoped>
$red: #d30320;
.mixwrapper {
    height: inherit;
    @media only screen and (min-width: 640px) {
        height: 95%;
    }
    display: grid;
    grid-template-columns: auto;
    grid-gap: 5px;
    grid-auto-rows: 0.1fr 0.8fr 0.1fr;
    grid-template-areas: 
        "t"
        "a"
        "c";
    .topItem {
        grid-area: t;
        height: inherit;
        @media only screen and (max-width: 640px) {
            height: 0 !important;
            display: none;
        }
        .header {
            background: rgba(#1e1e1f, 0.7);
            outline: none;
            border: none;
            border-radius: 5rem;
            cursor: pointer;
            // -webkit-transform:rotate(90deg);
            height: 30px;
            width: 120px;
            font-size: 15px;
            text-transform: uppercase;
            font-weight: 700;
            color: #e9c9a9;
            font-family: 'Dancing Script'
        }
    }
    .item1 {
        grid-area: a;
        overflow-y: scroll;
        overflow-x: hidden;
        height: inherit;
    }
    .item3 {
        grid-area: c;
        height: inherit;
        &.bar {
            input {
                width: 30px !important;
            }
            display: flex;
            flex-direction: column;
            justify-content: space-around;
        }
    }
}
.lockCls {
    background: transparent;
    outline: none;
    border: none;
}
.loading {
    cursor: default !important;
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
</style>