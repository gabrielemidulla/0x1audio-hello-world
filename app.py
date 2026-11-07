import ox1audio as ox


@ox.screen("Hello")
def hello(name: ox.Text):
    who = name.strip() if isinstance(name, str) and name.strip() else "world"
    return {"message": f"Hello, {who}"}


if __name__ == "__main__":
    ox.run()
