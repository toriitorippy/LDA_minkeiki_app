<template>
  <div>
    <div class ='home1'>
    <br>
    <div class='title'>民経記LDA</div>
    <br>
    </div>
    <div style="margin: 100px 0;"></div>
        <b-container>
          <b-row>
        <b-col cols='3'>
          <el-card>
            <div style="margin: 10px 0;"></div>
            <p>Topic画面</p>
            <img src="../assets/topic.png" class="image">
            <div style="padding: 14px;">
              <span>Topic画面では、各トピックの情報を見ることができます。語句と人名の上位30,時系列変化,上位文章に分かれています。クリックで他の画面に遷移できます。</span>
            </div>
          </el-card>
        </b-col>
        <b-col cols='3'>
          <el-card>
            <div style="margin: 10px 0;"></div>
            <p>Text画面</p>
            <img src="../assets/text.png" class="image">
            <div style="padding: 14px;">
              <span>Text画面では、各文章の情報を見ることができます。ロードに10秒程かかります。サイドバーから見たい文章を選んでください。</span>
            </div>
          </el-card>
        </b-col>
          <b-col cols='3'>
          <el-card>
            <div style="margin: 10px 0;"></div>
            <p>Word画面</p>
            <img src="../assets/word.png" class="image">
            <div style="padding: 14px;">
              <span>Word画面では、各単語の情報を見ることができます。左上の検索フォームからBag-of-Wordsに含まれている民経記中単語を入力してください。</span>
            </div>
          </el-card>
        </b-col>
          <b-col cols='3'>
          <el-card>
            <div style="margin: 10px 0;"></div>
            <p>Setting画面</p>
            <img src="../assets/setting.png" class="image">
            <div style="padding: 14px;">
              <span>Setting画面では、トピック数を変化させることができます。新たにLDAを実行する設定は未実装です。</span>
            </div>
          </el-card>
        </b-col>
    </b-row>
    </b-container>
  </div>
</template>

<script>
// import axios from 'axios'
// import {BACKEND_URL} from '../../util/const'

export default {
  name: 'home',
  components: {
  },
  mounted () {
    this.getData()
  },
  data() {
    return {
      activeName: 1,
      number_of_topic:10,
    };
  },
  methods: {
}
}
</script>

<style>
  .home1 {
    background: linear-gradient(-45deg, rgba(246, 255, 0, .8), rgba(255, 0, 161, .8)) fixed,
    url("http://www.webcreatorbox.com/sample/images/bg-cherrybrossam.jpg");
    background-size: cover;
  }

  .title {
    font-size: 80px;
    color: white;
    text-align: left;
  }
    .time {
    font-size: 13px;
    color: #999;
  }
  
  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .button {
    padding: 0;
    float: right;
  }

  .image {
    width: 100%;
    display: block;
  }

  .clearfix:before,
  .clearfix:after {
      display: table;
      content: "";
  }
  
  .clearfix:after {
      clear: both
  }
</style>