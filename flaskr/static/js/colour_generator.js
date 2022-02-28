function colour_generator(num_colours) {
  if (num_colours <= 0) return;
  colours = [];
  for(var i=0; i < num_colours; i++) {
    // Generate random hexadecimal colour
    colours.push("#" + (Math.random() * 0xfffff * 1000000)
        .toString(16)
        .slice(0, 6));
  }
  return colours;
}
