<template>
    <div class="mixwrapper">
        <div class="topItem">
            <input type="button" value="Style Mixing" class="header loading" @click="showStyleMix=!showStyleMix"/>
        </div>
        <div class="item1 thinScroll">
            <checkbox-picker :initMax="5" v-on:checkedInit="onCheckedInit" v-on:checked="onMixLayerPicked"></checkbox-picker>
        </div>
        <div class="item2 thinScroll">
            <scroll-gallery :mixImgs="mixImgs" :selectedImgIdx="selectedImgIdx" @onMiximgClick="onMiximgClick"></scroll-gallery>
        </div>
        <div class="item3">
            <div class="bar">
                <button type="button" class="lockCls" v-b-tooltip.hover :title="isLocked?'Locked Current Style':'Click to lock this style'"> 
                <i v-if="!isLocked" class='fas fa-lock-open fa-fw' @click="lockMixStyle"></i> 
                <i v-if="isLocked" class='fas fa-lock fa-fw'></i> 
                </button>
                <button type="button" class="lockCls loading" v-b-tooltip.hover :title="isMixing?'Mixing':'Completed'"> 
                    <i v-if="!isMixing" class='fas fa-check fa-fw'></i> 
                    <i v-if="isMixing" class='fas fa-spinner fa-spin fa-fw'></i> 
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import scrollGallery from '@/components/VerticalScrollImg.vue';
import checkboxPicker from '@/components/CheckboxPicker.vue';
import { mapState, mapActions, mapMutations } from 'vuex'
    export default {
        name:"stylemixMenu",
        components: {
            checkboxPicker: checkboxPicker,
            scrollGallery: scrollGallery
        },
        computed: mapState({
            isConnected: state => state.socketStore.isConnected,
            galleryMixImgs: state => state.socketStore.galleryMixImgs,
            cleared: state => state.socketStore.cleared,
            mainFaceImg: state => state.socketStore.mainFaceImg,
        }),
        watch: {
            mainFaceImg:  {
                handler: function(n, o) {
                    if(this.isMixing) {
                        this.isMixing = false;
                    }
                },
                deep: true,
                immediate: true
            },
            galleryMixImgs:  {
                handler: function(n, o) {
                    this.loadGallery(n);
                },
                deep: true,
                immediate: true
            },
            cleared: {
                handler: function(n, o) {
                    if(n) {
                        this.clear(n);
                    }
                },
                deep: true,
                immediate: true
            },
            isConnected: {
                handler: function(n, o) {
                    if(n) {
                        this.isMixing = true;
                    }
                },
                deep: true,
                immediate: true
            }
        },
        data() {
            return {
                mixImgs: ["1", "2", "3", "4", "5"],
                layersMixMap: [],
                selectedImgIdx: 0,
                isLocked: true,
                isMixing: false
            }
        },
        mounted() {
            this.onMiximgClick(0);
        },
        methods: {
            ... mapActions('socketStore', [
                'sendEditAction'
            ]),
            clear(flag) {

            },
            loadGallery(imgArr) {
                if(imgArr == null) return;
                this.mixImgs = imgArr;
            },
            onCheckedInit(vals) {
                this.layersMixMap = vals;
            },
            onMiximgClick(imgIdx) {
                this.selectedImgIdx = imgIdx;
                let params = {"styleImgIdx": imgIdx, "layersMixMap": this.layersMixMap};
                let msg = {};
                msg.action = "mixStyleImg";
                msg.params = params;
                this.sendEditAction(msg);
                this.isLocked = false;
                this.isMixing = true;
            },
            onMixLayerPicked(vals) {
                this.layersMixMap = vals;
                let params = {"styleImgIdx": this.selectedImgIdx, "layersMixMap": this.layersMixMap};
                let msg = {};
                msg.action = "mixStyleImg";
                msg.params = params;
                this.sendEditAction(msg);
                this.isLocked = false;
                this.isMixing = true;
            },
            lockMixStyle() {
                let params = {};
                let msg = {};
                msg.action = "lockStyle";
                msg.params = params;
                this.sendEditAction(msg);
                this.isLocked = true;
                this.$ga.event('category', 'btnClick', 'lockMixStyle', 1);
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
    grid-template-columns: 0.3fr 0.7fr;
    grid-gap: 5px;
    grid-auto-rows: auto;
    grid-template-areas: 
        "t t"
        "a b"
        "c c";
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
    .item2 {
        grid-area: b;
        overflow-y: scroll;
        height: inherit;
    }
    .item3 {
        grid-area: c;
        height: inherit;
        &.bar {
            display: flex;
            flex-direction: row;
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