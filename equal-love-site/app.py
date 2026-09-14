from pathlib import Path
import os
import sqlite3

from flask import Flask, abort, flash, g, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "instance" / "love_reviews.db"

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "equal-love-local-development-key"),
    DATABASE=DATABASE,
)
# データの中身を内包リストで管理
ALBUMS = [
    (1, "＝LOVE 7th ANNIVERSARY PREMIUM CONCERT", "Type-C", "2025.05.21", "c.png", "LIVE Blu-ray", "7周年コンサートの熱気を収めたType-C。ステージ全体の空気感まで楽しめる映像作品です。"),
    (2, "＝LOVE 7th ANNIVERSARY PREMIUM CONCERT", "Type-B", "2025.05.21", "b.png", "LIVE Blu-ray", "7周年コンサートのType-B。お気に入りのシーンや演出について感想を共有できます。"),
    (3, "＝LOVE 7th ANNIVERSARY PREMIUM CONCERT", "Type-A", "2025.05.21", "a.png", "LIVE Blu-ray", "7周年コンサートのType-A。ライブならではの表情とパフォーマンスを味わえる一枚です。"),
    (4, "とくべチュ、して／恋人以上、好き未満", "CD Only / Type-F", "2025.02.26", "F.jpg", "17th Single", "表題曲2曲を収録したCD Only盤。楽曲、歌詞、歌声の好きなところをレビューできます。"),
    (5, "とくべチュ、して／恋人以上、好き未満", "CD+Blu-ray / Type-E", "2025.02.26", "E.jpg", "17th Single", "期間生産限定盤Type-E。収録内容を含めた感想を残せます。"),
    (6, "とくべチュ、して／恋人以上、好き未満", "CD+Blu-ray / Type-D", "2025.02.26", "D.jpg", "17th Single", "Type-Dの収録内容やビジュアルについてレビューを共有できます。"),
    (7, "とくべチュ、して／恋人以上、好き未満", "CD+DVD / Type-C", "2025.02.26", "C.jpg", "17th Single", "Type-C。何度も聴きたくなるポイントをファン同士で共有しましょう。"),
    (8, "とくべチュ、して／恋人以上、好き未満", "CD+DVD / Type-B", "2025.02.26", "B.jpg", "17th Single", "Type-B。楽曲や映像の印象を星評価とコメントで記録できます。"),
    (9, "とくべチュ、して／恋人以上、好き未満", "CD+DVD / Type-A", "2025.02.26", "A.jpg", "17th Single", "Type-A。あなたのお気に入りの一曲や見どころを教えてください。"),
    (10, "イコノイジョイ 2023", "Type-C", "2024.09.18", "C3.jpg", "LIVE Blu-ray", "イコノイジョイ2023を収録したType-C。忘れられない場面をレビューできます。"),
    (11, "イコノイジョイ 2023", "Type-B", "2024.09.18", "B2.jpg", "LIVE Blu-ray", "イコノイジョイ2023 Type-B。ライブの魅力をファンの言葉で残せます。"),
    (12, "イコノイジョイ 2023", "Type-A", "2024.09.18", "A1.jpg", "LIVE Blu-ray", "イコノイジョイ2023 Type-A。パフォーマンスや演出の感想を共有できます。"),
]

NEWS_ITEMS = [
    ("2025.09.11", "MEDIA", "【出演情報】日本テレビ「THE 突破ファイル」※齋藤樹愛羅、野口衣織"),
    ("2025.09.11", "LIVE", "＝LOVE 8周年ツアー 沖縄公演 プレイガイド受付開始のお知らせ"),
    ("2025.09.10", "LIVE", "8周年ツアー 千葉・愛知・北海道公演 一般先行チケット受付開始"),
    ("2025.09.10", "STREAM", "「イコノイジョイ大感謝祭 2025」〈2部〉配信チケット発売"),
    ("2025.09.10", "MEDIA", "TOブックス『悪役令嬢ですが攻略対象の様子が異常すぎる』7巻 ※野口衣織"),
    ("2025.09.09", "MEDIA", "宝島社『sweet 11月号』※大谷映美里"),
    ("2025.09.09", "LIVE", "LAWSON 50th Anniversary Special LIVE FC先行受付開始"),
    ("2025.09.08", "GOODS", "「イコノイジョイ大感謝祭 2025」物販情報"),
    ("2025.09.08", "RELEASE", "「イコノイジョイ 2024」映像商品アートワーク・収録内容公開"),
    ("2025.09.08", "EVENT", "19thシングル発売記念オンライン個別お話し会 第4次～第6次応募受付"),
    ("2025.09.08", "MEDIA", "Rakuten GirlsAward 2025 AUTUMN/WINTER 出演情報"),
    ("2025.09.06", "STREAM", "リスパ『ラブソングに襲われる』配信記念企画を実施"),
]

SCHEDULE = [
    ("2025.11.02", "千葉", "LaLa arena TOKYO-BAY", "OPEN 13:30 / START 15:00"),
    ("2025.11.01", "千葉", "LaLa arena TOKYO-BAY", "OPEN 13:00 / START 15:00"),
    ("2025.10.12", "宮城", "ゼビオアリーナ仙台", "OPEN 13:30 / START 15:00"),
    ("2025.10.11", "宮城", "ゼビオアリーナ仙台", "OPEN 14:30 / START 16:00"),
    ("2025.10.04", "沖縄", "沖縄コンベンションセンター", "OPEN 12:30 / START 14:00"),
    ("2025.10.03", "沖縄", "沖縄コンベンションセンター", "OPEN 14:30 / START 16:00"),
    ("2025.09.27–28", "山梨", "富士急ハイランド・コニファーフォレスト", "OPEN 15:00 / START 16:30"),
    ("2025.09.07", "広島", "広島サンプラザホール", "OPEN 13:30 / START 15:00"),
    ("2025.09.06", "広島", "広島サンプラザホール", "OPEN 14:30 / START 16:00"),
]

# 公式プロフィールの公開情報を、画面で使いやすい形にまとめています。
# URLは「公式プロフィールを見る」リンクにだけ使用します。
MEMBERS = [
    {
        "number": "01",
        "name": "大谷 映美里",
        "roman": "OTANI EMIRI",
        "birthday": "1998.03.15",
        "from": "東京都",
        "height": "155cm",
        "blood": "O型",
        "profile": "メイクやファッション、ラーメン巡りが趣味。特技はジョッキ持ち。",
        "image": "members/otani_emiri.jpg",
        "social_url": "https://x.com/otani_emiri",
        "url": "https://equal-love.jp/feature/otani_emiri",
    },
    {
        "number": "02",
        "name": "大場 花菜",
        "roman": "OBA HANA",
        "birthday": "2000.02.04",
        "from": "埼玉県",
        "height": "160cm",
        "blood": "A型",
        "profile": "舞台・ミュージカル観劇とレトロなものが好き。イラストと書道が特技。",
        "image": "members/hana_oba.jpg",
        "social_url": "https://x.com/hana_oba",
        "url": "https://equal-love.jp/feature/oba_hana",
    },
    {
        "number": "03",
        "name": "音嶋 莉沙",
        "roman": "OTOSHIMA RISA",
        "birthday": "1998.08.11",
        "from": "福岡県",
        "height": "160cm",
        "blood": "B型",
        "profile": "コスメ集めや食べ歩きが趣味。フラフープと福岡愛を語ることが特技。",
        "image": "members/otoshima_risa.jpg",
        "social_url": "https://x.com/otoshima_risa",
        "url": "https://equal-love.jp/feature/otoshima_risa",
    },
    {
        "number": "04",
        "name": "齋藤 樹愛羅",
        "roman": "SAITO KIARA",
        "birthday": "2004.11.26",
        "from": "栃木県",
        "height": "156.2cm",
        "blood": "B型",
        "profile": "ゲームとカラオケ、メイク動画が好き。立ちブリッジやモノマネが特技。",
        "image": "members/saitou_kiara.jpg",
        "social_url": "https://x.com/saitou_kiara",
        "url": "https://equal-love.jp/feature/saito_kiara",
    },
    {
        "number": "05",
        "name": "佐々木 舞香",
        "roman": "SASAKI MAIKA",
        "birthday": "2000.01.21",
        "from": "愛知県",
        "height": "157cm",
        "blood": "A型",
        "profile": "趣味は寝ること。絡まったネックレスをほどくことが特技。",
        "image": "members/sasaki_maika.jpg",
        "social_url": "https://x.com/sasaki_maika",
        "url": "https://equal-love.jp/feature/sasaki_maika",
    },
    {
        "number": "06",
        "name": "髙松 瞳",
        "roman": "TAKAMATSU HITOMI",
        "birthday": "2001.01.19",
        "from": "東京都",
        "height": "163cm",
        "blood": "AB型",
        "profile": "映画・ドラマ鑑賞が趣味。特技はバトントワリング。",
        "image": "members/takamatsuhitomi.jpg",
        "social_url": "https://x.com/takamatsuhitomi",
        "url": "https://equal-love.jp/feature/takamatsu_hitomi",
    },
    {
        "number": "07",
        "name": "瀧脇 笙古",
        "roman": "TAKIWAKI SHOKO",
        "birthday": "2001.07.09",
        "from": "神奈川県",
        "height": "158cm",
        "blood": "O型",
        "profile": "料理、ヘアアレンジ、横浜散策が趣味。マラソンが特技。",
        "image": "members/shoko_takiwaki.jpg",
        "social_url": "https://x.com/shoko_takiwaki",
        "url": "https://equal-love.jp/feature/takiwaki_shoko",
    },
    {
        "number": "08",
        "name": "野口 衣織",
        "roman": "NOGUCHI IORI",
        "birthday": "2000.04.26",
        "from": "茨城県",
        "height": "161cm",
        "blood": "O型",
        "profile": "アニメ、漫画、ゲームと動画鑑賞が趣味。",
        "image": "members/noguchi_iori.jpg",
        "social_url": "https://x.com/noguchi_iori",
        "url": "https://equal-love.jp/feature/noguchi_iori",
    },
    {
        "number": "09",
        "name": "諸橋 沙夏",
        "roman": "MOROHASHI SANA",
        "birthday": "1996.08.03",
        "from": "福島県",
        "height": "158cm",
        "blood": "B型",
        "profile": "映画鑑賞が趣味。フラダンスとタヒチアンダンスが特技。",
        "image": "members/morohashi_sana.jpg",
        "social_url": "https://x.com/morohashi_sana",
        "url": "https://equal-love.jp/feature/morohashi_sana",
    },
    {
        "number": "10",
        "name": "山本 杏奈",
        "roman": "YAMAMOTO ANNA",
        "birthday": "1997.11.30",
        "from": "広島県",
        "height": "149.5cm",
        "blood": "A型",
        "profile": "スポーツ観戦、ダンス、料理が趣味。目分量料理が特技。",
        "image": "members/yamamoto_anna_.jpg",
        "social_url": "https://x.com/yamamoto_anna_",
        "url": "https://equal-love.jp/feature/yamamoto_anna",
    },
]

# ネット上の文章は転載せず、作品情報や公開レポートを参考に書いた例文です。
# seed_keyを付けることで、アプリを再起動しても同じレビューが重複しません。
SAMPLE_REVIEWS = [
    ("sample-01", 1, "レビュー例 01", 5, "会場の幸福感まで伝わる", "大きなステージを使った演出とメンバーの表情がしっかり残っていて、家でもコンサートの熱量を味わえました。生演奏に負けない歌声が特に印象的です。", "2026-08-26 19:20:00"),
    ("sample-02", 1, "レビュー例 02", 4, "何度も見返したいライブ映像", "かわいい曲から歌唱力を聴かせる曲まで流れが良く、あっという間に最後まで見られました。客席の空気も映るので、その日に参加したような気持ちになります。", "2026-08-20 21:05:00"),
    ("sample-03", 2, "レビュー例 03", 3, "特典までじっくり楽しめる", "ライブ本編の華やかさはもちろん、Type-Bならではの内容も楽しめました。画角の切り替えは好みが分かれそうですが、メンバーの細かな表情はよく伝わります。", "2026-08-12 18:40:00"),
    ("sample-04", 3, "レビュー例 04", 5, "7周年の集大成", "これまでの歩みとこれからの勢いを同時に感じる作品でした。力強い歌声、華やかな衣装、会場との一体感がそろっていて、最後には自然と拍手したくなります。", "2026-08-03 20:10:00"),
    ("sample-05", 4, "レビュー例 05", 5, "甘い世界観がぎゅっと詰まっている", "両A面の二曲は同じ恋でも違う距離感を描いていて、続けて聴くと歌詞のつながりまで楽しめます。明るいメロディーが耳に残る一枚です。", "2026-07-29 17:30:00"),
    ("sample-06", 4, "レビュー例 06", 3, "曲を中心に楽しみたい人向け", "CD Onlyなので映像はありませんが、曲そのものを繰り返し聴きたい人には分かりやすい構成です。歌詞カードを見ながら聴くと細かな言葉遊びにも気づけました。", "2026-07-18 22:15:00"),
    ("sample-07", 5, "レビュー例 07", 4, "かわいさと物語を両方楽しめる", "楽曲の甘い雰囲気と映像のストーリーがよく合っています。メンバーらしさが見える場面が多く、曲を聴いたあとに映像をもう一度見たくなりました。", "2026-07-11 19:45:00"),
    ("sample-08", 6, "レビュー例 08", 3, "ジャケットの雰囲気が好き", "曲のかわいさに合ったビジュアルで、手元に置きたくなるデザインです。映像特典はもう少し長く見たかったものの、全体として満足できました。", "2026-07-02 20:50:00"),
    ("sample-09", 7, "レビュー例 09", 5, "カップリングまで強い", "表題曲だけでなく収録曲も個性があり、通して聴いても飽きません。特にテンポの良い曲はライブで盛り上がる様子まで想像できました。", "2026-06-28 18:25:00"),
    ("sample-10", 7, "レビュー例 10", 4, "映像を見るともっと好きになる", "歌だけでも十分かわいいですが、映像と合わせると表情や振り付けの魅力が増します。友達に最初の一枚としてすすめやすい内容だと思います。", "2026-06-21 21:15:00"),
    ("sample-11", 8, "レビュー例 11", 2, "楽曲は好き、特典は好み次第", "二つの表題曲はどちらも耳に残り、何度も聴きたくなります。一方で、このTypeの映像特典は自分の好みとは少し違ったので、購入前に各形態を比べるのがおすすめです。", "2026-06-13 16:40:00"),
    ("sample-12", 9, "レビュー例 12", 4, "王道のかわいさを楽しめる", "明るく甘い曲調と、少しもどかしい恋心の組み合わせがイコラブらしいです。声の重なりもきれいで、サビを聴くたびに元気になれます。", "2026-06-06 20:05:00"),
    ("sample-13", 9, "レビュー例 13", 3, "初めて聴く人にも入りやすい", "印象に残る言葉と覚えやすいメロディーで、初めて聴いてもすぐ楽しめました。曲数をもっと聴きたい気持ちは残りますが、入口として良い一枚です。", "2026-05-28 19:10:00"),
    ("sample-14", 10, "レビュー例 14", 5, "三組の個性が一つになる瞬間", "グループごとの色の違いと、全員が集まったときの大きなエネルギーを一度に楽しめます。会場の広さを生かした演出にもわくわくしました。", "2026-05-20 22:00:00"),
    ("sample-15", 10, "レビュー例 15", 4, "お祭り感のあるライブ", "次々に曲がつながっていくので、家で見ても気分が上がります。好きなグループだけでなく、ほかの二組の魅力を知るきっかけにもなりました。", "2026-05-12 18:30:00"),
    ("sample-16", 11, "レビュー例 16", 2, "全景をもう少し見たかった", "出演者の表情はよく見えましたが、個人的にはフォーメーションが分かる全体映像も多いとうれしかったです。それでも三組が作る特別な空気は十分楽しめました。", "2026-05-03 20:25:00"),
    ("sample-17", 12, "レビュー例 17", 5, "大切な夏の記録", "ステージ上の楽しそうな表情と客席の盛り上がりが伝わり、見終わったあとに爽やかな余韻が残りました。何度でも戻りたくなるライブ作品です。", "2026-04-24 19:55:00"),
    ("sample-18", 12, "レビュー例 18", 4, "推し以外にも目が向く作品", "人数の多いステージでも見どころが整理されていて、それぞれのグループやメンバーの良さを発見できました。休日にゆっくり見返したいです。", "2026-04-16 21:35:00"),
]

# db接続の関数化
def get_db():
    if "db" not in g:
        # gに接続を保存すると、同じリクエスト中は一つの接続を使い回せます。
        Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

# エラー受けかな？、あとで読む
# エラー吐いたらdb閉じてるっぽい
@app.teardown_appcontext
def close_db(_error=None):
    database = g.pop("db", None)
    if database is not None:
        database.close()

# dbの初期化、起動時にdb中身のチェックと不足分生成
def init_db():
    database = get_db()
    database.executescript((BASE_DIR / "schema.sql").read_text(encoding="utf-8"))

    # 以前のデータベースを持っている場合だけ、不足している列を後から追加します。
    # PRAGMA table_infoで現在の列名を調べるため、何度起動しても重複追加されません。
    review_columns = {
        row["name"] for row in database.execute("PRAGMA table_info(reviews)").fetchall()
    }
    if "is_sample" not in review_columns:
        database.execute(
            "ALTER TABLE reviews ADD COLUMN is_sample INTEGER NOT NULL DEFAULT 0"
        )
    if "seed_key" not in review_columns:
        database.execute("ALTER TABLE reviews ADD COLUMN seed_key TEXT")
    database.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_reviews_seed_key
        ON reviews(seed_key) WHERE seed_key IS NOT NULL
        """
    )
    database.executemany(
        """
        INSERT OR IGNORE INTO albums
        (id, title, edition, release_date, image, category, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        ALBUMS,
    )
    database.executemany(
        """
        INSERT OR IGNORE INTO reviews
        (seed_key, album_id, nickname, rating, review_title, comment, created_at, is_sample)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        """,
        SAMPLE_REVIEWS,
    )
    # インデックス情報をSQLiteへ伝え、検索時の実行計画を最適化します。
    database.execute("PRAGMA optimize")
    database.commit()

# ここからflaskの部分
# 基本上のdb関数周り読み出してrender-templateに渡してるだけ

@app.route("/")
def index():
    albums = get_db().execute(
        """
        SELECT albums.*, COUNT(reviews.id) AS review_count,
               ROUND(AVG(reviews.rating), 1) AS average_rating
        FROM albums LEFT JOIN reviews ON reviews.album_id = albums.id
        GROUP BY albums.id ORDER BY albums.release_date DESC, albums.id LIMIT 3
        """
    ).fetchall()
    return render_template("index.html", albums=albums, news=NEWS_ITEMS[:4], show_intro=True)


@app.route("/news")
def news():
    return render_template("news.html", news=NEWS_ITEMS)


@app.route("/members")
def members():
    return render_template("members.html", members=MEMBERS)


@app.route("/discography")
def discography():
    # LEFT JOINにより、レビューが0件の作品も一覧から消えないようにしています。
    albums = get_db().execute(
        """
        SELECT albums.*, COUNT(reviews.id) AS review_count,
               ROUND(AVG(reviews.rating), 1) AS average_rating
        FROM albums LEFT JOIN reviews ON reviews.album_id = albums.id
        GROUP BY albums.id ORDER BY albums.release_date DESC, albums.id
        """
    ).fetchall()
    return render_template("discography.html", albums=albums)

# アルバムのデータ読み出し部分、中身なかったら404に飛ばしてる
def get_album_or_404(album_id):
    album = get_db().execute(
        """
        SELECT albums.*, COUNT(reviews.id) AS review_count,
               ROUND(AVG(reviews.rating), 1) AS average_rating
        FROM albums LEFT JOIN reviews ON reviews.album_id = albums.id
        WHERE albums.id = ? GROUP BY albums.id
        """,
        (album_id,),
    ).fetchone()
    # 飛ばす部分
    if album is None:
        abort(404)
    return album


@app.route("/discography/<int:album_id>")
def album_detail(album_id):
    album = get_album_or_404(album_id)
    reviews = get_db().execute(
        "SELECT * FROM reviews WHERE album_id = ? ORDER BY created_at DESC, id DESC",
        (album_id,),
    ).fetchall()
    return render_template("album_detail.html", album=album, reviews=reviews)

# レビューのルールチェック、正規化するべきではある
def validate_review(form):
    nickname = form.get("nickname", "").strip()
    review_title = form.get("review_title", "").strip()
    comment = form.get("comment", "").strip()
    try:
        rating = int(form.get("rating", "0"))
    except ValueError:
        rating = 0

    if not 1 <= len(nickname) <= 30:
        return None, "ニックネームは1〜30文字で入力してください。"
    if rating not in range(1, 6):
        return None, "星1〜5の評価を選んでください。"
    if not 1 <= len(review_title) <= 60:
        return None, "レビュータイトルは1〜60文字で入力してください。"
    if not 10 <= len(comment) <= 800:
        return None, "感想は10〜800文字で入力してください。"
    return (nickname, rating, review_title, comment), None


@app.post("/discography/<int:album_id>/reviews")
def add_review(album_id):
    get_album_or_404(album_id)
    values, error = validate_review(request.form)
    if error:
        flash(error, "error")
        return redirect(url_for("album_detail", album_id=album_id) + "#review-form")

    database = get_db()
    database.execute(
        "INSERT INTO reviews (album_id, nickname, rating, review_title, comment) VALUES (?, ?, ?, ?, ?)",
        (album_id, *values),
    )
    database.commit()
    flash("レビューを投稿しました。あなたの言葉がレビュー一覧に加わりました。", "success")
    return redirect(url_for("album_detail", album_id=album_id) + "#reviews")


@app.route("/reviews/<int:review_id>/edit", methods=("GET", "POST"))
def edit_review(review_id):
    database = get_db()
    review = database.execute("SELECT * FROM reviews WHERE id = ?", (review_id,)).fetchone()
    if review is None:
        abort(404)
    album = get_album_or_404(review["album_id"])
    if review["is_sample"]:
        flash("サンプルレビューは編集できません。", "error")
        return redirect(url_for("album_detail", album_id=review["album_id"]) + "#reviews")

    if request.method == "POST":
        values, error = validate_review(request.form)
        if error:
            flash(error, "error")
        else:
            database.execute(
                """
                UPDATE reviews SET nickname = ?, rating = ?, review_title = ?, comment = ?,
                    updated_at = datetime('now', 'localtime') WHERE id = ?
                """,
                (*values, review_id),
            )
            database.commit()
            flash("レビューを更新しました。", "success")
            return redirect(url_for("album_detail", album_id=review["album_id"]) + "#reviews")

    return render_template("edit_review.html", album=album, review=review)


@app.post("/reviews/<int:review_id>/delete")
def delete_review(review_id):
    database = get_db()
    review = database.execute(
        "SELECT album_id, is_sample FROM reviews WHERE id = ?", (review_id,)
    ).fetchone()
    if review is None:
        abort(404)
    if review["is_sample"]:
        flash("サンプルレビューは削除できません。", "error")
        return redirect(url_for("album_detail", album_id=review["album_id"]) + "#reviews")
    database.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
    database.commit()
    flash("レビューを削除しました。", "success")
    return redirect(url_for("album_detail", album_id=review["album_id"]) + "#reviews")


@app.route("/special")
def special():
    return render_template("special.html", schedule=SCHEDULE)


@app.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html"), 404


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
