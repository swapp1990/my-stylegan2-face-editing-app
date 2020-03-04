<template>
<div class="wrapper">
    <div class="main-head"><logoHeading></logoHeading></div>
    <div class="galleryWrapper">
        <fractalGrid :galleryImgs="galleryImgs"></fractalGrid>
    </div>
</div>
</template>
<script>
import fractalGrid from '@/components/FractalGrid.vue';
import logoHeading from '@/components/LogoHeading.vue';
    export default {
        name: "GalleryMobile",
        components: {
            fractalGrid: fractalGrid,
            logoHeading: logoHeading,
        },
        data() {
            return {
                galleryImgs: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            }
        },
        mounted() {
        }
    }
</script>

<style lang="scss" scoped>
</style>