<template>
    <div class="search-box">
        <i class='fas fa-search icon'></i>
        <input type="text" placeholder="hair is brown" @keyup="clicked" v-model="text">
    </div>
</template>

<script>
    export default {
        name: "searchExpand",
        props: ['propText'],
        data: () => {
            return {
                text: ""
            }
        },
        mounted() {
            
        },
        methods: {
            clicked(e) {
                // console.log(this.text);
                if(e.key == "Enter") {
                    this.$emit("onEnter", this.text);
                }
            }
        }
    }
</script>

<style scoped lang="scss">
$primary: #0077FF;
$dark: #00104B;
$shadow-tl: -4px -2px 4px 0px;
$shadow-br: 4px 2px 6px 0px;
$white: #ffffff;
$dark: rgb(234, 223, 234);
$pink: rgb(216, 20, 223);
$shadow: $shadow-tl $white, $shadow-br $dark;
$shadow-flip: $shadow-tl $dark inset, $shadow-br $white inset;
    .search-box {
        outline: none;
        border: none;
        box-shadow: $shadow;
        display: inline-block;
        position: relative;
        border-radius: 10px;
        input[type="text"] {
            font-family: Raleway, sans-serif;
            font-size: 20px;
            font-weight: bold;
            width: 30px;
            height: 30px;
            padding: 5px 40px 5px 10px;
		    border: none;
            box-sizing: border-box;
            border-radius: 10px;
            // transition: width 800ms cubic-bezier(0.5,-0.5,0.5,0.5) 600ms;
            background: rgba($pink,.03);
            // &:hover {
            //     background: rgba($dark,.03);
            // }
            &:focus {
                outline: none;
                + span {
                    color: rgba($dark,.03);
                }
                width: 300px;
                @media only screen and (max-width: 640px) {
                    width: 200px;
                }
                transition: width 800ms cubic-bezier(0.5, -0.5, 0.5, 1.5);
                border-radius: 50px;
                // box-shadow: 2px 2px 2px 0px $dark inset, -2px -2px 2px 0px $white inset;
            }
            &:not(:focus) {
                transition: width 300ms cubic-bezier(0.5, -0.5, 0.5, 1.5);
                border-radius: 10px;
            }
        }
        .icon {
            position: absolute;
            pointer-events: none;
            right: 10px;
            top: 8px;
        }
    }
</style>