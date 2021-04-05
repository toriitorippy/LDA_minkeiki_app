# LDA_minkeiki_app
このアプリは卒業論文及び情報処理学会発表用に作成したアプリケーションのデモとなります。
LDA(Latent Dirichlet Allocation)と呼ばれるトピックモデルを鎌倉中期の公家の日記である『民経記』に適用し、文書の有用性・わかりやすさ・アクセス性を向上させました。
著作権のため、『民経記』のすべてを公開することができず、Text画面は一部（デモ）となります。

## アプリケーションリンク
[https://minkeiki-app.azurewebsites.net/](https://minkeiki-app.azurewebsites.net/)

##　システム概要
システムの概要は随時追加していきます。

# docker立ち上げ
vueのパッケージインストール
※node_modulesとyarn.lockがない状態か確認
```
docker-compose run vue yarn
```

vueとflaskのbuild
```
docker-compose build
```

docker立ち上げ
```
docker-compose up vue
```