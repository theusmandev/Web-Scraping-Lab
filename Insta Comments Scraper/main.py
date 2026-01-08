

import instaloader
import csv
import time

def scrape_anonymous():
    print("\n--- 🕵️ Anonymous Scraper (No Login) ---\n")
    
    # Koi login nahi, bas simple loader
    L = instaloader.Instaloader()

    # Post Shortcode (URL se: DSsGIk4CF2K)
    shortcode = "DSsGIk4CF2K"

    try:
        print(f"⏳ Fetching Post {shortcode} anonymously...")
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        print(f"📝 Owner: {post.owner_username}")
        print(f"💬 Total Comments: {post.comments}")
        print("\n⬇️ Scraping Started...\n")

        comments_data = []
        count = 0

        for comment in post.get_comments():
            comments_data.append({
                "username": comment.owner.username,
                "text": comment.text
            })
            count += 1
            print(f"[{count}] {comment.owner.username}: {comment.text[:30]}")

            # Bohot slow speed taake pakre na jayen
            if count % 20 == 0:
                print("⏳ Sleeping 5 seconds...")
                time.sleep(5)

        # Save
        filename = f"comments_{shortcode}_anon.csv"
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["username", "text"])
            writer.writeheader()
            writer.writerows(comments_data)

        print(f"\n✅ DONE! {count} comments saved.")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nNateja: Agar ye fail hua, to Instagram ne apka IP Address block kar dia ha.")

if __name__ == "__main__":
    scrape_anonymous()