<template>
    <div class="wrapper">
    <div class="wrapper-grid">
        <div class="header">A</div>
        <div class="side-menu-l">B1</div>
        <div class="main-body">B</div>
        <div class="side-menu-r">B2</div>
        <div class="btm-menu">bottom menu</div>
        <div class="footer">C</div>
    </div>
</div>
</template>

<script>
    export default {
        
    }
</script>

<style lang="scss" scoped>
%commonLayoutOptsMobile {
    padding: 20px;
    margin: 10px;
    @media only screen and (max-width: 640px) {
        padding: 5px;
        margin: 5px;
    }
}
.wrapper {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
}
.wrapper-grid {
    width: 80vw;
    height: 100vh;
    display: grid;
    grid-gap: 10px;
    @media only screen and (max-width: 640px) {
        grid-gap: 2px;
        width: 100vw;
    }
    grid-template-columns: 0.8fr 2.4fr 0.8fr;
    grid-template-rows: 1fr 1fr 1fr 1fr;
    grid-template-areas:
        "header header header"
        "sml mb smr"
        "bm bm bm"
        "footer footer footer";
    background-color: #444;
    color: #444;
}
.header {
    @extend %commonLayoutOptsMobile;
    background-color: #fff;
    grid-area: header;
    border-radius: 5px;
}
.side-menu-l {
    @extend %commonLayoutOptsMobile;
    background-color: #fff;
    grid-area: sml;
    border-radius: 5px;
}
.main-body {
    @extend %commonLayoutOptsMobile;
    background-color: #fff;
    grid-area: mb;
    border-radius: 5px;
}
.side-menu-r {
    @extend %commonLayoutOptsMobile;
    background-color: #fff;
    grid-area: smr;
    border-radius: 5px;
}
.btm-menu {
    @extend %commonLayoutOptsMobile;
    background-color: #fff;
    grid-area: bm;
    border-radius: 5px;
}
.footer {
    @extend %commonLayoutOptsMobile;
    background-color: #fff;
    grid-area: footer;
    border-radius: 5px;
}
</style>