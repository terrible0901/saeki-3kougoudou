document.addEventListener("DOMContentLoaded", () => {
  const intro = document.querySelector(".site-intro");
  if (intro) window.setTimeout(() => intro.classList.add("is-finished"), 3300);

  // 画面内へ入った要素だけを表示し、最初から全要素を動かす負荷を避けます。
  const revealItems = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -6%" });
    revealItems.forEach((item, index) => {
      item.style.transitionDelay = `${Math.min(index % 4, 3) * 70}ms`;
      observer.observe(item);
    });
  } else {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  }

  const menuButton = document.querySelector(".menu-button");
  const navigation = document.querySelector(".global-nav");
  if (menuButton && navigation) {
    menuButton.addEventListener("click", () => {
      const open = document.body.classList.toggle("nav-open");
      menuButton.setAttribute("aria-expanded", String(open));
      menuButton.querySelector(".sr-only").textContent = open ? "メニューを閉じる" : "メニューを開く";
    });
    navigation.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => {
      document.body.classList.remove("nav-open");
      menuButton.setAttribute("aria-expanded", "false");
    }));
  }

  // 星をクリックしたとき、数字だけでなく評価の言葉もすぐに表示します。
  document.querySelectorAll(".star-picker").forEach((picker) => {
    const output = picker.parentElement.querySelector(".rating-output");
    picker.querySelectorAll("input").forEach((input) => {
      input.addEventListener("change", () => {
        if (output) output.textContent = `${input.value} / 5 — ${ratingLabel(Number(input.value))}`;
      });
    });
  });

  document.querySelectorAll("textarea[maxlength]").forEach((textarea) => {
    const counter = textarea.parentElement.querySelector(".char-count");
    const updateCount = () => {
      if (counter) counter.textContent = `${textarea.value.length} / ${textarea.maxLength}`;
    };
    textarea.addEventListener("input", updateCount);
    updateCount();
  });

  document.querySelectorAll("form[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!window.confirm(form.dataset.confirm)) event.preventDefault();
    });
  });

  document.querySelectorAll(".review-form").forEach((form) => {
    form.addEventListener("submit", () => {
      const submit = form.querySelector(".submit-button");
      if (submit) {
        submit.disabled = true;
        submit.firstChild.textContent = "送信中 ";
      }
    });
  });

  document.querySelectorAll(".flash").forEach((flash) => {
    const dismiss = () => {
      flash.style.opacity = "0";
      window.setTimeout(() => flash.remove(), 250);
    };
    flash.querySelector("button")?.addEventListener("click", dismiss);
    window.setTimeout(dismiss, 5200);
  });

  // dialog要素を使うと、Escキーでも拡大画像を閉じられます。
  const dialog = document.querySelector(".lightbox");
  if (dialog && "HTMLDialogElement" in window) {
    document.querySelectorAll("[data-lightbox-src]").forEach((button) => {
      button.addEventListener("click", () => {
        dialog.querySelector("img").src = button.dataset.lightboxSrc;
        dialog.showModal();
      });
    });
    dialog.querySelector("button").addEventListener("click", () => dialog.close());
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) dialog.close();
    });
  }

  // サイト内ページへ移る直前にピンクの幕を表示します。
  // 同じページ内のリンクや外部サイトへのリンクは通常どおり動かします。
  document.querySelectorAll("a[href]").forEach((link) => {
    link.addEventListener("click", (event) => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || link.target === "_blank") return;
      const destination = new URL(link.href, window.location.href);
      const samePageAnchor = destination.pathname === window.location.pathname && destination.hash;
      if (destination.origin !== window.location.origin || samePageAnchor) return;
      event.preventDefault();
      document.body.classList.add("is-leaving");
      window.setTimeout(() => { window.location.href = destination.href; }, 420);
    });
  });
});

function ratingLabel(value) {
  return { 1: "もうひとつ", 2: "まずまず", 3: "好き", 4: "とても好き", 5: "大好き！" }[value] || "";
}
