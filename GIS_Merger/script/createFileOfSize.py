with open("sync/filebig2w", "wb") as out:
    out.seek((1024 * 1024 * 1024) - 1)
    out.write('\0')