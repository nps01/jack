def two_to_one(two_tuple, width) -> int:
    """map 2-space to 1-space
    """
    x, y = two_tuple
    return width * x + y + 1

def one_to_two(n, width) -> (int, int):
    """map 1-space to 2-space
    """
    return (n//width - int(n % width == 0), (n - 1) % width)

def find_neighbors(index, width, height, pixels, reach) -> list:
    """find all neighbors
    1) map point in 1-space to 2-space
    2) add all possible combinations of offsets <= reach
        to compute a pixels "neighborhood"
    3) map the neighborhood back to 1-space and find the pixel value
        at each index.
    """
    x, y = one_to_two(index, width)
    neighborhood = set() # lazy way to filter duplicates
    # generate neighborhood - set of all neighbors.
    for i in range(0, reach+1):
        for j in range(0, reach+1):
            neighborhood.add((x-i, y+j))
            neighborhood.add((x+i, y-j))
            neighborhood.add((x-i, y-j))
            neighborhood.add((x+i, y+j))
    # filter impossible neighbors
    neighborhood = [(i,j) for i,j in neighborhood if 0 <= i < height and 0 <= j < width]
    # map 2-tuples back to integers, subtract 1 to create valid indicies.
    neighborhood =  [two_to_one((i,j), width) - 1 for i,j in neighborhood]
    # find pixel value of each neighbor
    return [pixels[i] for i in neighborhood]

def median(arr):
    """sort array with mergesort, then calculate the median
        improvements: 
        1) for len(arr) <= 20 insertion sort might be faster; idk worth testing.
           for instance the reach parameter in denoise is greter than 2 maybe stick
           with merge.
        2) the code given in the assignment arr[len(arr)//2] only computes the median
           for lists with odd lengths.  The following function correctly 
           calculates the median for even and odd length lists.
    """
    merge_sort(arr)
    return (arr[len(arr)//2] + arr[len(arr)//2 - int(len(arr) % 2 == 0)])/2

def merge_sort(arr):
    if len(arr) > 1:
 
        # Finding middle of input list
        m = len(arr)//2
 
        # Bifurcate input list 
        L, R = arr[:m], arr[m:]
 
        # Sort each half recursively
        merge_sort(L)
        merge_sort(R)
 
        i, j, k = 0, 0, 0
 
        # Copy elements from arr to L & R
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
 
        # Final while loops check for leftover elements.
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
 
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def denoise_image(pixels, width, height, reach = 2, beta = 0.2):
    """if abs(original - median) / (original + 0.1) > beta, replace pixel
    ***
    this function assumes pixels has been transformed prior to invokation
    [i,i,i ...] -> [i, ...]
    remove redundancy in pixel list.
    """
    from copy import deepcopy
    new_pixels = deepcopy(pixels)

    for i in range(len(pixels)):
        neighbors = find_neighbors(i, width, height, pixels, reach)
        med = median(neighbors)
        if abs(pixels[i] - med)/ (pixels[i]+ 0.1) > beta:
            new_pixels[i] = med
    return new_pixels


def create_pixels(read_this):
    """
    improvements:
    - when opening a file use the with keyword.
        adds error handling & auto closes file.
    - no need to read all 3 integers from each line,
         because image in black & white the rgb channels
         all have the same value.  Reading all 3 values 
         triples your memory requirement.
    """
    f = open(read_this, 'r')
    p3 = f.readline()
    pixel_list = []

    while True:
        line = f.readline()
        if line == '':
            break
        line_list = line.split()
        for pix_str in line_list:
            pixel_list.append(int(pix_str))
    f.close()
    return pixel_list

def test():
    name = "cat.ppm"
    data = create_pixels(name)
    width, height, maxval = data[0:3]
    pixels = data[3:]

    # reduce the pixel list, we only need 1 channel.
    r_pixels = [pixels[i] for i in range(0, len(pixels), 3)]
    print(width, height, maxval)
    new_pixels = denoise_image(r_pixels, width, height)
    print("new: ",new_pixels)


if __name__ == "__main__": test()

