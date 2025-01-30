import sys
import os
import time
import logging
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from src.request import get_linkedin_jobs
from src.filter import word_search_strict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def search_jobs():
    job_name = job_name_entry.get()
    location = location_entry.get()
    if not job_name or not location:
        messagebox.showwarning("Input Error", "Please enter both job name and location.")
        logging.warning("Input Error: Job name or location not provided.")
        return
    
    logging.info(f"Searching jobs for: {job_name} in {location}")
    
    # Start loading animation
    start_loading_animation()

    # Run job search in a separate thread
    threading.Thread(target=perform_job_search, args=(job_name, location)).start()

def perform_job_search(job_name, location):
    jobs = get_linkedin_jobs(job_name, location)
    
    # Stop loading animation
    stop_loading_animation()

    if jobs is None:
        messagebox.showinfo("No Results", "No jobs found. Please try again.")
        logging.info("No jobs found.")
        return
    
    job_listbox.delete(0, tk.END)
    for job in jobs:
        job_listbox.insert(tk.END, job)
    logging.info(f"Found {len(jobs)} jobs.")

def start_loading_animation():
    global loading, loading_canvas, loading_angle
    loading = True
    loading_canvas = tk.Canvas(frame, width=50, height=50, bg="black", highlightthickness=0)
    loading_canvas.grid(row=3, column=0, columnspan=2)
    loading_angle = 0
    animate_loading()
    logging.info("Started loading animation.")

def stop_loading_animation():
    global loading
    loading = False
    loading_canvas.grid_forget()
    logging.info("Stopped loading animation.")

def animate_loading():
    global loading, loading_canvas, loading_angle
    if loading:
        loading_canvas.delete("all")
        loading_canvas.create_arc(10, 10, 40, 40, start=loading_angle, extent=90, fill="white")
        loading_angle = (loading_angle + 10) % 360
        loading_canvas.after(100, animate_loading)

def main():
    global job_name_entry, location_entry, job_listbox, frame

    root = tk.Tk()
    root.title("Job Scraper")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Job Name:", foreground="black").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    job_name_entry = ttk.Entry(frame, width=30, background="white", foreground="black")
    job_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    ttk.Label(frame, text="Location:", foreground="black").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    location_entry = ttk.Entry(frame, width=30, background="white", foreground="black")
    location_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    search_button = ttk.Button(frame, text="Search", command=search_jobs)
    search_button.grid(row=2, column=0, columnspan=2, pady=10)

    job_listbox = tk.Listbox(frame, width=50, height=15, foreground="black")
    job_listbox.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    logging.info("Starting Job Scraper application.")
    main()
    logging.info("Job Scraper application closed.")