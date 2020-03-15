<template>
<div class="pick-wrapper">
  <ul class="ks-cboxtags">
    <li v-for="val in values">
        <input type="checkbox" :id="val.id" v-model='val.checked' @change="changeVals()">
        <!-- <label :for="val.id" @click="clickOnLabel(val)">{{val.id}}</label> -->
        <label @click="clickOnLabel(val)" v-b-tooltip.hover :title="val.hoverText">{{val.id}}</label>
    </li>
  </ul>
</div>
</template>

<script>
    export default {
        name: "checkboxPicker",
        props: {
            initMax: {
                type: Number,
                default: 9
            },
        },
        data() {
            return {
                minRange: 0,
                maxRange: 13,
                values: []
            }
        },
        mounted() {
            this.checkedValues();
        },
        methods: {
            checkedValues() {
                for(let i = 0; i < this.maxRange; i++) {
                    let checkedVal = false;
                    if(i < this.initMax) {
                        checkedVal = true;
                    }
                    let text = 'Mix Face Shape and Orientation'
                    if (i > 3) {
                        text = 'Mix Hairstyles and Hair Color'
                    } 
                    if(i > 7) {
                        text = 'Mix Face Texture'
                    }
                    if(i > 10) {
                        text = 'Mix Finer Details'
                    }

                    this.values.push({id: i, checked: checkedVal, hoverText: text})
                }
                this.$emit('checkedInit', this.values);
            },
            changeVals() {
                this.$emit('checked', this.values);
            },
            clickOnLabel(val) {
                // console.log("click ", val.checked);
                val.checked = !val.checked;
                this.$emit('checked', this.values);
            }
        }
    }
</script>

<style lang="scss" scoped>
.pick-wrapper {
    max-width: 200px;
    max-height: 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 13px;
    display: grid;
    grid-template-rows: 0.25fr;
    grid-gap: 5px;
}

ul.ks-cboxtags {
    list-style: none;
    padding: 5px;
    @media only screen and (max-width: 640px) {
        padding: 0px;
    }
}
ul.ks-cboxtags li{
  display: inline;
}
ul.ks-cboxtags li label{
    display: inline-block;
    background-color: rgba(255, 255, 255, .9);
    border: 2px solid rgba(139, 139, 139, .3);
    color: #adadad;
    border-radius: 25px;
    white-space: nowrap;
    margin: 1px 0px;
    @media only screen and (max-width: 640px) {
        margin: 0;
    }
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
    transition: all .2s;
}

ul.ks-cboxtags li label {
    padding: 2px 6px;
    @media only screen and (max-width: 640px) {
        padding: 0;
    }
    cursor: pointer;
}

ul.ks-cboxtags li label::before {
    display: inline-block;
    font-style: normal;
    font-variant: normal;
    text-rendering: auto;
    -webkit-font-smoothing: antialiased;
    font-family: "Font Awesome 5 Free";
    font-weight: 900;
    font-size: 10px;
    padding: 1px 3px 1px 1px;
    @media only screen and (max-width: 640px) {
        padding: 0;
    }
    content: "\f067";
    transition: transform .3s ease-in-out;
}

ul.ks-cboxtags li input[type="checkbox"]:checked + label::before {
    content: "\f00c";
    transform: rotate(-360deg);
    transition: transform .3s ease-in-out;
}

ul.ks-cboxtags li input[type="checkbox"]:checked + label {
    // border: 2px solid #1bdbf8;
    background-color: #f31a1ed1;
    color: #fff;
    transition: all .2s;
}

ul.ks-cboxtags li input[type="checkbox"] {
  display: absolute;
}
ul.ks-cboxtags li input[type="checkbox"] {
  position: absolute;
  opacity: 0;
}
ul.ks-cboxtags li input[type="checkbox"]:focus + label {
  border: 2px solid #e9a1ff;
}
</style>