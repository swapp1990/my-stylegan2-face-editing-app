<template>
    <div class="neubox" :style="{height: h+'px',width: w+'px'}">
        <slot></slot>
    </div>
</template>

<script>
    export default {
        name: "neubox",
        props: ["proph", "propw"],
        data() {
            return {
                h: 600,
                w: 600
            }
        },
        mounted() {
            if(this.proph) this.h = this.proph;
            if(this.propw) this.w = this.propw;
            this.w = this.propw;
            this.adjustSize();
        },
        methods: {
           adjustSize() {
               if (window.innerWidth < 720) {
                   this.h = 600;
                   this.w = 500;
               }
           }
        }
    }
</script>

<style lang="scss" scoped>
$radius: 3px;
$white: #ffffff;
$dark: #DFE4EA;
$shadow-tl: -4px -2px 4px 0px;
$shadow-br: 4px 2px 6px 0px;
$shadow: $shadow-tl $white, $shadow-br $dark;
.neubox {
    background-color: #f5f6f7;
    // padding: 1rem 1.5rem;
    border-radius: $radius;
    box-shadow: $shadow;
    // margin: auto;
    margin-right: 0;
    margin-left: 0;
}
</style>