<template>
    <div class="mixwrapper">
        <div class="item1 thinScroll">
            <checkbox-picker :initMax="5" v-on:checkedInit="onCheckedInit" v-on:checked="onMixLayerPicked"></checkbox-picker>
        </div>
        <div class="item2 thinScroll">
            <scroll-gallery :mixImgs="mixImgs" :selectedImgIdx="selectedImgIdx" @onMiximgClick="onMiximgClick"></scroll-gallery>
        </div>
        <div class="item3">
            <button type="button" class="lockCls"> 
                <i v-if="!isLocked" class='fas fa-lock-open fa-fw' @click="lockMixStyle"></i> 
                <i v-if="isLocked" class='fas fa-lock fa-fw'></i> 
            </button>
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
            galleryMixImgs: state => state.socketStore.galleryMixImgs,
            cleared: state => state.socketStore.cleared
        }),
        watch: {
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
            }
        },
        data() {
            return {
                mixImgs: ["1", "2", "3", "4", "5"],
                layersMixMap: [],
                selectedImgIdx: 0,
                isLocked: true
            }
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
            },
            onMixLayerPicked(vals) {
                this.layersMixMap = vals;
                let params = {"styleImgIdx": this.selectedImgIdx, "layersMixMap": this.layersMixMap};
                let msg = {};
                msg.action = "mixStyleImg";
                msg.params = params;
                this.sendEditAction(msg);
                this.isLocked = false;
            },
            lockMixStyle() {
                let params = {};
                let msg = {};
                msg.action = "lockStyle";
                msg.params = params;
                this.sendEditAction(msg);
                this.isLocked = true;
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
        "a b"
        "c c";
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
    }
}
.lockCls {
    background: transparent;
    outline: none;
    border: none;
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