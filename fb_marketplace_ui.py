import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from fb_marketplace_lister import MarketplaceLister

class MarketplaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FB Marketplace Auto Lister")
        self.root.geometry("600x750")

        self.profile_path = tk.StringVar()
        self.image_paths = []

        self.create_widgets()

    def create_widgets(self):
        # 1. Profile Selection
        profile_frame = tk.LabelFrame(self.root, text="Chrome Profile Selection", padx=10, pady=10)
        profile_frame.pack(fill="x", padx=10, pady=5)

        tk.Entry(profile_frame, textvariable=self.profile_path, width=50).pack(side="left", padx=5)
        tk.Button(profile_frame, text="Browse Profile Folder", command=self.browse_profile).pack(side="left")

        # 2. Listing Details
        details_frame = tk.LabelFrame(self.root, text="Listing Details", padx=10, pady=10)
        details_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Title
        tk.Label(details_frame, text="Title:").grid(row=0, column=0, sticky="w", pady=2)
        self.title_entry = tk.Entry(details_frame, width=40)
        self.title_entry.grid(row=0, column=1, sticky="w", pady=2)

        # Price
        tk.Label(details_frame, text="Price (USD):").grid(row=1, column=0, sticky="w", pady=2)
        self.price_entry = tk.Entry(details_frame, width=15)
        self.price_entry.grid(row=1, column=1, sticky="w", pady=2)

        # Category
        tk.Label(details_frame, text="Category:").grid(row=2, column=0, sticky="w", pady=2)
        self.category_combo = ttk.Combobox(details_frame, values=list(MarketplaceLister.CATEGORY_MAP.keys()), state="readonly", width=37)
        self.category_combo.grid(row=2, column=1, sticky="w", pady=2)
        if list(MarketplaceLister.CATEGORY_MAP.keys()):
            self.category_combo.current(2) # Default to Household

        # Condition
        tk.Label(details_frame, text="Condition:").grid(row=3, column=0, sticky="w", pady=2)
        self.condition_combo = ttk.Combobox(details_frame, values=["New", "Used - Like New", "Used - Good", "Used - Fair"], state="readonly", width=37)
        self.condition_combo.grid(row=3, column=1, sticky="w", pady=2)
        self.condition_combo.current(2)

        # Location
        tk.Label(details_frame, text="Location:").grid(row=4, column=0, sticky="w", pady=2)
        self.location_entry = tk.Entry(details_frame, width=40)
        self.location_entry.grid(row=4, column=1, sticky="w", pady=2)

        # Door Meetup
        self.door_meetup_var = tk.BooleanVar(value=True)
        tk.Checkbutton(details_frame, text="Offer Door Meetup/Dropoff", variable=self.door_meetup_var).grid(row=5, column=0, columnspan=2, sticky="w", pady=2)

        # Description
        tk.Label(details_frame, text="Description:").grid(row=6, column=0, sticky="nw", pady=2)
        self.desc_text = tk.Text(details_frame, height=8, width=40)
        self.desc_text.grid(row=6, column=1, sticky="w", pady=2)

        # 3. Image Selection
        img_frame = tk.LabelFrame(self.root, text="Images", padx=10, pady=10)
        img_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(img_frame, text="Select Images", command=self.select_images).pack(side="left", padx=5)
        self.img_label = tk.Label(img_frame, text="No images selected", fg="gray")
        self.img_label.pack(side="left", padx=5)

        # 4. Action Buttons
        action_frame = tk.Frame(self.root)
        action_frame.pack(fill="x", padx=10, pady=15)

        self.draft_btn = tk.Button(action_frame, text="Draft Listing", command=lambda: self.start_listing("draft"), bg="orange", fg="white", font=("Arial", 12, "bold"))
        self.draft_btn.pack(side="left", expand=True, fill="x", padx=5)

        self.publish_btn = tk.Button(action_frame, text="Publish Listing", command=lambda: self.start_listing("publish"), bg="green", fg="white", font=("Arial", 12, "bold"))
        self.publish_btn.pack(side="left", expand=True, fill="x", padx=5)

        # Status
        self.status_lbl = tk.Label(self.root, text="Ready", fg="blue")
        self.status_lbl.pack(pady=5)

    def browse_profile(self):
        folder = filedialog.askdirectory(title="Select Chrome Profile Directory")
        if folder:
            self.profile_path.set(folder)

    def select_images(self):
        files = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if files:
            self.image_paths = list(files)
            self.img_label.config(text=f"{len(self.image_paths)} image(s) selected", fg="black")

    def start_listing(self, action):
        if not self.profile_path.get():
            messagebox.showerror("Error", "Please select a Chrome Profile folder.")
            return

        if not self.title_entry.get():
            messagebox.showerror("Error", "Title is required.")
            return

        try:
            float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for Price.")
            return

        template_data = {
            "title": self.title_entry.get(),
            "price": self.price_entry.get(),
            "category": self.category_combo.get(),
            "condition": self.condition_combo.get(),
            "location": self.location_entry.get(),
            "door_meetup": self.door_meetup_var.get(),
            "description": self.desc_text.get("1.0", tk.END).strip(),
            "images": self.image_paths,
            "availability": "List as Single Item"
        }

        profile_dir = self.profile_path.get()

        self.status_lbl.config(text=f"Starting automation... Action: {action.upper()}", fg="orange")
        self.draft_btn.config(state="disabled")
        self.publish_btn.config(state="disabled")

        # Run in a separate thread so GUI doesn't freeze
        threading.Thread(target=self.run_lister, args=(profile_dir, template_data, action), daemon=True).start()

    def run_lister(self, profile_dir, template_data, action):
        lister = MarketplaceLister()
        success = lister.create_listing(profile_dir, template_data, action=action)

        if success:
            self.root.after(0, lambda: self.status_lbl.config(text=f"Success! Listing {action}ed.", fg="green"))
            self.root.after(0, lambda: messagebox.showinfo("Success", f"Listing successfully {action}ed!"))
        else:
            self.root.after(0, lambda: self.status_lbl.config(text="Failed! Check console for errors.", fg="red"))
            self.root.after(0, lambda: messagebox.showerror("Error", "Failed to process listing. Check console for details."))

        self.root.after(0, lambda: self.draft_btn.config(state="normal"))
        self.root.after(0, lambda: self.publish_btn.config(state="normal"))

if __name__ == "__main__":
    root = tk.Tk()
    app = MarketplaceApp(root)
    root.mainloop()
