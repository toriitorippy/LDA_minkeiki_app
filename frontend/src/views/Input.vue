<template>
  <div>
    <div class="imgContent">
      <div class="imagePreview">
        <img :src="uploadedImage" style="width:100%;" />
      </div>
      <input type="file" class="file" name="file" @change="onFileChange" />
      <button @click='onUploadImage' name="file">画像判定してくだちい・・・</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import {BACKEND_URL} from '../../util/const'

export default {
  data () {
    return {
      uploadedImage: '',
      file: '',
    }
  },
  methods: {
    // 選択した画像を反映
    onFileChange (e) {
      this.file = e.target.files || e.dataTransfer.files
      let files = e.target.files || e.dataTransfer.files
      this.createImage(files[0])
    },
    // アップロードした画像を表示
    createImage (file) {
      let reader = new FileReader()
      reader.onload = (e) => {
        this.uploadedImage = e.target.result
      }
      reader.readAsDataURL(file)
    },
    // 画像をサーバーへアップロード
    onUploadImage () {
      var params = new FormData()
      params.append('uploadimage', this.uploadedImage)
      params.append('file', this.file[0])
      // Axiosを用いてFormData化したデータをFlaskへPostしています。
      axios.post(`${BACKEND_URL}/classification`, params).then(function (response) {
        console.log(response)
      })
    }
  }
}
</script>