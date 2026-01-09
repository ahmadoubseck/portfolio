def test_extract_title(self):
    md = "# Hello world\nSome text"
    self.assertEqual(extract_title(md), "Hello world")
